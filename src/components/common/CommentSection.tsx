import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { Loader2, MessageSquare, Send } from 'lucide-react';
import { toast } from '@/hooks/use-toast';
import { format } from 'date-fns';
import { useNavigate } from 'react-router-dom';
import api from '@/services/api';
import { UserProfile } from '@/contexts/AuthContext';

interface Comment {
  id: number;
  content: string;
  created_at: string;
  user_id: number;
  news_id?: number;
  event_id?: number;
  author?: UserProfile;
}

interface CommentSectionProps {
  contentType: 'news' | 'event';
  contentId: number;
}

const CommentSection: React.FC<CommentSectionProps> = ({ contentType, contentId }) => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchComments = useCallback(async () => {
    setIsLoading(true);
    try {
      const params = {
        [contentType === 'news' ? 'news_id' : 'event_id']: contentId,
        limit: 100, // Or some other limit
      };
      const response = await api.get<Comment[]>('/comments/', { params });
      setComments(response.data || []);
    } catch (error) {
      console.error('Error fetching comments:', error);
      toast({
        title: 'خطا در دریافت نظرات',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  }, [contentId, contentType]);

  useEffect(() => {
    fetchComments();
  }, [fetchComments]);

  const handleSubmitComment = async () => {
    if (!user) {
      toast({ title: 'برای ارسال نظر باید وارد شوید' });
      navigate('/login');
      return;
    }
    if (!newComment.trim()) {
      toast({ title: 'نظر خالی است', variant: 'destructive' });
      return;
    }

    setIsSubmitting(true);
    try {
      const commentData = {
        content: newComment,
        [contentType === 'news' ? 'news_id' : 'event_id']: contentId,
      };
      await api.post('/comments/', commentData);
      setNewComment('');
      toast({ title: 'نظر شما ثبت شد' });
      fetchComments(); // Refetch comments after submitting
    } catch (error: any) {
      console.error('Error submitting comment:', error);
      toast({
        title: 'خطا در ارسال نظر',
        description: error.response?.data?.detail || 'لطفا دوباره تلاش کنید',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="mt-8 space-y-6">
        <h3 className="text-xl font-bold flex items-center"><MessageSquare className="ml-2" /> نظرات</h3>
        <div className="flex gap-4">
            <Avatar><AvatarFallback>{user?.full_name?.charAt(0) || '?'}</AvatarFallback></Avatar>
            <div className="flex-1">
                <Textarea placeholder="نظر خود را بنویسید..." value={newComment} onChange={(e) => setNewComment(e.target.value)} />
                <Button onClick={handleSubmitComment} disabled={isSubmitting} className="mt-2">
                    {isSubmitting ? <Loader2 className="ml-2 h-4 w-4 animate-spin" /> : <Send className="ml-2 h-4 w-4" />}
                    ارسال
                </Button>
            </div>
        </div>
        <Separator />
        <div className="space-y-4">
            {isLoading ? <div className="text-center"><Loader2 className="h-8 w-8 animate-spin" /></div>
            : comments.length > 0 ? comments.map((comment) => (
                <div key={comment.id} className="bg-card p-4 rounded-lg">
                    <div className="flex items-center gap-3">
                        <Avatar><AvatarFallback>{comment.author?.full_name?.charAt(0) || '?'}</AvatarFallback></Avatar>
                        <div>
                            <p className="font-medium">{comment.author?.full_name}</p>
                            <p className="text-xs text-muted-foreground">{format(new Date(comment.created_at), 'yyyy/MM/dd HH:mm')}</p>
                        </div>
                    </div>
                    <p className="text-sm mt-2">{comment.content}</p>
                </div>
            )) : <p className="text-center text-muted-foreground">هنوز نظری ثبت نشده است.</p>}
        </div>
    </div>
  );
};

export default CommentSection;
