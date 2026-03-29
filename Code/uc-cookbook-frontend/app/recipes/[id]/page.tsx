'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import {
  getRecipeById,
  saveRecipeToCookbook,
  getStoredToken,
  getRecipeComments,
  addRecipeComment,
  deleteRecipeComment,
  setCommentReaction,
  startConversation,
  deleteRecipe,
} from '@/lib/api';
import { useAuth } from '@/lib/auth';
import type { Recipe, RecipeComment } from '@/lib/types';
import { UserAvatar } from '@/components/UserAvatar';
import {
  Clock,
  ChefHat,
  User,
  Calendar,
  BookmarkPlus,
  ArrowLeft,
  Loader2,
  MessageCircle,
  Share2,
  Send,
  Trash2,
  Reply,
  Pencil,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';

export default function RecipeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, user, setUser } = useAuth();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [comments, setComments] = useState<RecipeComment[]>([]);
  const [loading, setLoading] = useState(true);
  const [commentsLoading, setCommentsLoading] = useState(false);
  const [commentSubmitting, setCommentSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [replyingToId, setReplyingToId] = useState<number | null>(null);
  const [replyText, setReplyText] = useState('');
  const [reactionBusy, setReactionBusy] = useState<number | null>(null);
  const [deletingRecipe, setDeletingRecipe] = useState(false);

  const REACTION_EMOJIS = ['👍', '❤️', '😂', '🔥'] as const;

  useEffect(() => {
    if (params.id) {
      fetchRecipe();
    }
  }, [params.id]);

  const fetchRecipe = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getRecipeById(Number(params.id));
      setRecipe(data);
      await fetchComments();
    } catch (err: any) {
      setError(err.message || 'Failed to load recipe');
      console.error('Error fetching recipe:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchComments = async () => {
    try {
      setCommentsLoading(true);
      const data = await getRecipeComments(Number(params.id));
      setComments(data);
    } catch {
      setComments([]);
    } finally {
      setCommentsLoading(false);
    }
  };

  const handleSaveRecipe = async () => {
    if (!recipe || !isAuthenticated) return;

    // Guard: ensure token exists before calling API
    const token = getStoredToken();
    if (!token) {
      setUser(null);
      alert('Your session has expired. Please log in again to save recipes.');
      router.push('/auth/login');
      return;
    }
    try {
      setSaving(true);
      await saveRecipeToCookbook(recipe.id);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err: any) {
      // If it's a 401 error (unauthorized), clear auth and redirect to login
      if (err.status === 401 || err.message?.includes('Could not validate credentials')) {
        setUser(null);
        alert('Your session has expired. Please log in again to save recipes.');
        router.push('/auth/login');
        return;
      }
      alert(err.message || 'Failed to save recipe');
      console.error('Error saving recipe:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleAddComment = async () => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    if (!recipe || !newComment.trim()) return;

    try {
      setCommentSubmitting(true);
      await addRecipeComment(recipe.id, { content: newComment.trim() });
      setNewComment('');
      await fetchComments();
    } catch (err: any) {
      alert(err.message || 'Failed to add comment');
    } finally {
      setCommentSubmitting(false);
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    if (!recipe) return;
    try {
      await deleteRecipeComment(recipe.id, commentId);
      await fetchComments();
    } catch (err: any) {
      alert(err.message || 'Failed to delete comment');
    }
  };

  const handlePostReply = async () => {
    if (!recipe || replyingToId == null || !replyText.trim()) return;
    try {
      setCommentSubmitting(true);
      await addRecipeComment(recipe.id, {
        content: replyText.trim(),
        parent_id: replyingToId,
      });
      setReplyText('');
      setReplyingToId(null);
      await fetchComments();
    } catch (err: any) {
      alert(err.message || 'Failed to post reply');
    } finally {
      setCommentSubmitting(false);
    }
  };

  const handleToggleReaction = async (commentId: number, emoji: string) => {
    if (!recipe) return;
    try {
      setReactionBusy(commentId);
      await setCommentReaction(recipe.id, commentId, emoji);
      await fetchComments();
    } catch (err: any) {
      alert(err.message || 'Failed to update reaction');
    } finally {
      setReactionBusy(null);
    }
  };

  const childComments = (parentId: number | null) =>
    comments
      .filter((c) => (c.parent_id ?? null) === parentId)
      .sort(
        (a, b) =>
          new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      );

  const handleMessageAuthor = async () => {
    if (!recipe?.author_id) return;
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }
    if (user?.id === recipe.author_id) return;

    try {
      const conversation = await startConversation({ recipient_user_id: recipe.author_id });
      router.push(`/messages/${conversation.id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start conversation');
    }
  };

  const handleShareRecipe = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      alert('Recipe link copied to clipboard');
    } catch {
      alert('Unable to copy recipe link');
    }
  };

  const handleDeleteRecipe = async () => {
    if (!recipe) return;
    if (!confirm('Delete this recipe permanently? This cannot be undone.')) return;
    const token = getStoredToken();
    if (!token) {
      setUser(null);
      router.push('/auth/login');
      return;
    }
    try {
      setDeletingRecipe(true);
      await deleteRecipe(recipe.id);
      router.push('/');
    } catch (err: unknown) {
      const anyErr = err as { status?: number; message?: string };
      if (anyErr.status === 401 || anyErr.message?.includes('Could not validate credentials')) {
        setUser(null);
        router.push('/auth/login');
        return;
      }
      alert(anyErr.message || 'Failed to delete recipe');
    } finally {
      setDeletingRecipe(false);
    }
  };

  const difficultyColors = {
    easy: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    hard: 'bg-red-100 text-red-800',
  };

  if (loading) {
    return (
      <div className="container py-12 flex justify-center items-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (error || !recipe) {
    return (
      <div className="container py-12">
        <div className="max-w-md mx-auto text-center">
          <div className="bg-destructive/10 text-destructive rounded-lg p-6">
            <p className="font-medium">Error loading recipe</p>
            <p className="text-sm mt-1">{error || 'Recipe not found'}</p>
            <Button onClick={() => router.push('/')} variant="outline" className="mt-4">
              Back to Browse
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-8 md:py-12">
      <Button
        variant="ghost"
        onClick={() => router.back()}
        className="mb-6"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back
      </Button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Hero Image */}
          <div className="relative w-full h-[400px] rounded-lg overflow-hidden bg-muted">
            {recipe.image_url ? (
              <Image
                src={recipe.image_url}
                alt={recipe.title}
                fill
                className="object-cover"
                priority
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary/10 to-primary/5">
                <ChefHat className="h-32 w-32 text-primary/40" />
              </div>
            )}
          </div>

          {/* Title and Description */}
          <div>
            <h1 className="text-4xl font-bold tracking-tight mb-4">{recipe.title}</h1>
            <p className="text-lg text-muted-foreground">{recipe.description}</p>
          </div>

          {/* Meta Info */}
          <div className="flex flex-wrap items-center gap-4 pb-4 border-b">
            <div className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-muted-foreground" />
              <span className="font-medium">{recipe.time_minutes} minutes</span>
            </div>
            <Badge variant="outline" className={difficultyColors[recipe.difficulty]}>
              {recipe.difficulty}
            </Badge>
            {recipe.author && (
              <div className="flex items-center gap-2 text-muted-foreground">
                <User className="h-5 w-5" />
                <span>by {recipe.author.username}</span>
              </div>
            )}
            <div className="flex items-center gap-2 text-muted-foreground text-sm">
              <Calendar className="h-4 w-4" />
              <span>{new Date(recipe.created_at).toLocaleDateString()}</span>
            </div>
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-2">
            {recipe.tags.map((tag) => (
              <Badge key={tag} variant="secondary">
                {tag}
              </Badge>
            ))}
          </div>

          {/* Ingredients */}
          <Card>
            <CardHeader>
              <CardTitle>Ingredients</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {recipe.ingredients.map((ingredient, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="text-primary mt-1.5">•</span>
                    <span>{ingredient}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Steps */}
          <Card>
            <CardHeader>
              <CardTitle>Instructions</CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="space-y-4">
                {recipe.steps.map((step, index) => (
                  <li key={index} className="flex gap-4">
                    <span className="flex-shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-semibold text-sm">
                      {index + 1}
                    </span>
                    <p className="flex-1 pt-1">{step}</p>
                  </li>
                ))}
              </ol>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Comments</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {isAuthenticated ? (
                <div className="space-y-2">
                  <Textarea
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    placeholder="Add a comment..."
                    rows={3}
                  />
                  <Button onClick={handleAddComment} disabled={commentSubmitting || !newComment.trim()}>
                    <Send className="h-4 w-4 mr-2" />
                    {commentSubmitting ? 'Posting...' : 'Post Comment'}
                  </Button>
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">Log in to comment on this recipe.</p>
              )}

              {commentsLoading ? (
                <div className="flex items-center gap-2 text-muted-foreground text-sm">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Loading comments...
                </div>
              ) : comments.length === 0 ? (
                <p className="text-sm text-muted-foreground">No comments yet.</p>
              ) : (
                <div className="space-y-1">
                  {(() => {
                    const renderThread = (parentId: number | null, depth: number) => {
                      return childComments(parentId).map((comment) => {
                        const canDelete =
                          user &&
                          (user.id === comment.user_id || user.id === recipe.author_id);
                        const name = comment.user?.username || 'User';
                        const rx = comment.reactions ?? [];
                        return (
                          <div
                            key={comment.id}
                            className={depth > 0 ? 'ml-4 sm:ml-8 pl-3 border-l-2 border-muted mt-3' : 'mt-3'}
                          >
                            <div className="rounded-lg border p-3 bg-card">
                              <div className="flex gap-3">
                                <UserAvatar username={name} size="sm" />
                                <div className="min-w-0 flex-1">
                                  <div className="flex items-start justify-between gap-2">
                                    <div>
                                      <p className="text-sm font-medium">{name}</p>
                                      <p className="text-xs text-muted-foreground">
                                        {new Date(comment.created_at).toLocaleString()}
                                      </p>
                                    </div>
                                    <div className="flex items-center gap-1 shrink-0">
                                      {isAuthenticated && (
                                        <Button
                                          variant="ghost"
                                          size="sm"
                                          className="h-8 px-2"
                                          onClick={() => {
                                            setReplyingToId(
                                              replyingToId === comment.id ? null : comment.id
                                            );
                                            setReplyText('');
                                          }}
                                        >
                                          <Reply className="h-3.5 w-3.5 mr-1" />
                                          Reply
                                        </Button>
                                      )}
                                      {canDelete && (
                                        <Button
                                          variant="ghost"
                                          size="icon"
                                          className="h-8 w-8"
                                          onClick={() => handleDeleteComment(comment.id)}
                                        >
                                          <Trash2 className="h-4 w-4" />
                                        </Button>
                                      )}
                                    </div>
                                  </div>
                                  <p className="text-sm mt-2 whitespace-pre-wrap">{comment.content}</p>
                                  <div className="flex flex-wrap items-center gap-1 mt-3">
                                    {REACTION_EMOJIS.map((emoji) => {
                                      const summary = rx.find((r) => r.emoji === emoji);
                                      const count = summary?.count ?? 0;
                                      const active = summary?.reacted_by_me ?? false;
                                      return (
                                        <button
                                          key={emoji}
                                          type="button"
                                          disabled={!isAuthenticated || reactionBusy === comment.id}
                                          onClick={() => handleToggleReaction(comment.id, emoji)}
                                          className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs transition-colors ${
                                            active
                                              ? 'border-primary bg-primary/10'
                                              : 'border-transparent bg-muted/60 hover:bg-muted'
                                          }`}
                                        >
                                          <span>{emoji}</span>
                                          {count > 0 && <span className="text-muted-foreground">{count}</span>}
                                        </button>
                                      );
                                    })}
                                  </div>
                                  {isAuthenticated && replyingToId === comment.id && (
                                    <div className="mt-3 space-y-2">
                                      <Textarea
                                        value={replyText}
                                        onChange={(e) => setReplyText(e.target.value)}
                                        placeholder="Write a reply..."
                                        rows={2}
                                      />
                                      <div className="flex gap-2">
                                        <Button
                                          size="sm"
                                          onClick={handlePostReply}
                                          disabled={commentSubmitting || !replyText.trim()}
                                        >
                                          Post reply
                                        </Button>
                                        <Button
                                          size="sm"
                                          variant="outline"
                                          onClick={() => {
                                            setReplyingToId(null);
                                            setReplyText('');
                                          }}
                                        >
                                          Cancel
                                        </Button>
                                      </div>
                                    </div>
                                  )}
                                </div>
                              </div>
                            </div>
                            {renderThread(comment.id, depth + 1)}
                          </div>
                        );
                      });
                    };
                    return <>{renderThread(null, 0)}</>;
                  })()}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="sticky top-20 space-y-4">
            {isAuthenticated && (
              <Card>
                <CardContent className="pt-6">
                  <Button
                    onClick={handleSaveRecipe}
                    disabled={saving || saved}
                    className="w-full"
                    size="lg"
                  >
                    {saving ? (
                      <>
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                        Saving...
                      </>
                    ) : saved ? (
                      <>
                        <BookmarkPlus className="mr-2 h-5 w-5" />
                        Saved!
                      </>
                    ) : (
                      <>
                        <BookmarkPlus className="mr-2 h-5 w-5" />
                        Save to My Cookbook
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>
            )}

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Quick Info</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Prep Time</span>
                  <span className="font-medium">{recipe.time_minutes} min</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Difficulty</span>
                  <span className="font-medium capitalize">{recipe.difficulty}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Ingredients</span>
                  <span className="font-medium">{recipe.ingredients.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Steps</span>
                  <span className="font-medium">{recipe.steps.length}</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {isAuthenticated && user?.id === recipe.author_id && (
                  <>
                    <Button
                      type="button"
                      variant="outline"
                      className="w-full"
                      onClick={() => router.push(`/recipes/${recipe.id}/edit`)}
                    >
                      <Pencil className="h-4 w-4 mr-2" />
                      Edit recipe
                    </Button>
                    <Button
                      type="button"
                      variant="destructive"
                      className="w-full"
                      disabled={deletingRecipe}
                      onClick={handleDeleteRecipe}
                    >
                      {deletingRecipe ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Deleting...
                        </>
                      ) : (
                        <>
                          <Trash2 className="h-4 w-4 mr-2" />
                          Delete recipe
                        </>
                      )}
                    </Button>
                  </>
                )}
                {isAuthenticated && user?.id !== recipe.author_id && (
                  <Button onClick={handleMessageAuthor} className="w-full" variant="outline">
                    <MessageCircle className="h-4 w-4 mr-2" />
                    Message Author
                  </Button>
                )}
                <Button onClick={handleShareRecipe} className="w-full" variant="outline">
                  <Share2 className="h-4 w-4 mr-2" />
                  Share Recipe
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
