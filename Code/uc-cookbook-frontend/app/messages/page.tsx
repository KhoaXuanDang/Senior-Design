'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { getConversations } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import type { Conversation } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';

export default function ConversationsPage() {
  const router = useRouter();
  const { isAuthenticated, loading, user } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    if (isAuthenticated) {
      fetchConversations();
    }
  }, [isAuthenticated, loading]);

  const fetchConversations = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await getConversations();
      setConversations(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load conversations');
    } finally {
      setIsLoading(false);
    }
  };

  if (loading || isLoading) {
    return (
      <div className="container py-12 flex justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="container py-8 max-w-3xl">
      <h1 className="text-3xl font-bold mb-6">Conversations</h1>

      {error && <p className="text-destructive text-sm mb-4">{error}</p>}

      <div className="space-y-3">
        {conversations.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <p className="text-muted-foreground">No conversations yet.</p>
            </CardContent>
          </Card>
        ) : (
          conversations.map((conversation) => (
            <Card key={conversation.id}>
              <CardHeader>
                <CardTitle className="text-lg">
                  {user ? (
                    // Prefer showing username if API returned nested user objects
                    conversation.user_one?.username || conversation.user_two?.username ? (
                      `Conversation with ${
                        (conversation.user_one?.id === user.id ? conversation.user_two?.username : conversation.user_one?.username) || `user ${conversation.id}`
                      }`
                    ) : (
                      // Fallback to numeric id when username is not present
                      `Conversation with user ${
                        conversation.user_one_id === user.id ? conversation.user_two_id : conversation.user_one_id
                      }`
                    )
                  ) : (
                    `Conversation #${conversation.id}`
                  )}
                </CardTitle>
                <CardDescription>
                  Started {timeAgo(conversation.created_at)}{conversation.updated_at ? ` • updated ${timeAgo(conversation.updated_at)}` : ''}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">{new Date(conversation.updated_at || conversation.created_at).toLocaleString()}</p>
                <Button asChild>
                  <Link href={`/messages/${conversation.id}`} aria-label={`Open conversation ${conversation.id}`}>
                    Open
                  </Link>
                </Button>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}

function timeAgo(dateStr?: string) {
  if (!dateStr) return 'unknown';
  const then = new Date(dateStr).getTime();
  const diff = Date.now() - then;
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (seconds < 60) return `${seconds}s ago`;
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  return new Date(dateStr).toLocaleDateString();
}
