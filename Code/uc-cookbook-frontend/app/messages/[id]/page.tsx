'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { getConversationMessages, sendMessage } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import type { Message } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Loader2, Send } from 'lucide-react';

export default function ConversationMessagesPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, user, loading } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    if (isAuthenticated && params.id) {
      fetchMessages();
    }
  }, [isAuthenticated, loading, params.id]);

  const fetchMessages = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await getConversationMessages(Number(params.id));
      setMessages(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load messages');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim() || !params.id) return;

    try {
      setSending(true);
      await sendMessage(Number(params.id), { content: newMessage.trim() });
      setNewMessage('');
      await fetchMessages();
    } catch (err: any) {
      setError(err.message || 'Failed to send message');
    } finally {
      setSending(false);
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
      <Button variant="ghost" className="mb-4" onClick={() => router.push('/messages')}>
        Back to Conversations
      </Button>

      <Card>
        <CardHeader>
          <CardTitle>Conversation #{params.id}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && <p className="text-sm text-destructive">{error}</p>}

          <div className="space-y-2 max-h-[420px] overflow-y-auto pr-1">
            {messages.length === 0 ? (
              <p className="text-sm text-muted-foreground">No messages yet.</p>
            ) : (
              messages.map((message) => {
                const isMine = user?.id === message.sender_id;
                return (
                  <div
                    key={message.id}
                    className={`rounded-lg p-3 ${isMine ? 'bg-primary text-primary-foreground ml-8' : 'bg-muted mr-8'}`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <p className={`text-xs mt-2 ${isMine ? 'text-primary-foreground/80' : 'text-muted-foreground'}`}>
                      {new Date(message.created_at).toLocaleString()}
                    </p>
                  </div>
                );
              })
            )}
          </div>

          <div className="space-y-2">
            <Textarea
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type your message..."
              rows={3}
            />
            <Button onClick={handleSendMessage} disabled={sending || !newMessage.trim()}>
              <Send className="h-4 w-4 mr-2" />
              {sending ? 'Sending...' : 'Send'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
