import { useState, useCallback } from 'react';
import api from '@/services/api';
import { UserProfile, UserRole } from '@/contexts/AuthContext';
import { toast } from '@/hooks/use-toast';
import { Article } from '@/schemas/article'; // Assuming you have this schema defined based on backend
import { EventResponse } from '@/schemas/event'; // Assuming schema exists
import { News } from '@/schemas/news'; // Assuming schema exists

// We can define more specific types for admin data if needed
// For now, using the response schemas from backend is fine
type AdminUser = UserProfile;
type AdminAnnouncement = News;
type AdminEvent = EventResponse;
type AdminSubmission = Article;

export const useAdminData = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [announcements, setAnnouncements] = useState<AdminAnnouncement[]>([]);
  const [events, setEvents] = useState<AdminEvent[]>([]);
  const [submissions, setSubmissions] = useState<AdminSubmission[]>([]);

  const fetchData = useCallback(async (tab: string) => {
    setIsLoading(true);
    try {
      let response;
      switch (tab) {
        case 'users':
          response = await api.get('/users/');
          setUsers(response.data);
          break;
        case 'announcements':
          response = await api.get('/news/');
          setAnnouncements(response.data);
          break;
        case 'events':
          response = await api.get('/events/');
          setEvents(response.data);
          break;
        case 'submissions':
          response = await api.get('/articles/');
          setSubmissions(response.data);
          break;
      }
    } catch (error) {
      console.error(`Error fetching ${tab}:`, error);
      toast({
        title: 'خطا در بارگذاری اطلاعات',
        description: 'لطفا دوباره تلاش کنید',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleUpdateUserRole = async (userId: string, newRole: UserRole) => {
    try {
      const response = await api.put(`/users/${userId}/role`, { role: newRole });
      const updatedUser = response.data;

      setUsers(users.map(user =>
        user.id === updatedUser.id ? updatedUser : user
      ));

      toast({
        title: 'نقش کاربر بروزرسانی شد',
      });
    } catch (error: any) {
      console.error('Error updating user role:', error);
      toast({
        title: 'خطا در بروزرسانی نقش کاربر',
        description: error.response?.data?.detail || 'لطفا دوباره تلاش کنید',
        variant: 'destructive',
      });
    }
  };

  const handleUpdateSubmissionStatus = async (id: string, status: 'approved' | 'rejected') => {
    try {
      const response = await api.put(`/articles/${id}`, { status });
      const updatedSubmission = response.data;
      
      setSubmissions(submissions.map(submission =>
        submission.id === updatedSubmission.id ? updatedSubmission : submission
      ));

      toast({
        title: 'وضعیت مقاله بروزرسانی شد',
      });
    } catch (error: any) {
      console.error('Error updating submission status:', error);
      toast({
        title: 'خطا در بروزرسانی وضعیت مقاله',
        description: error.response?.data?.detail || 'لطفا دوباره تلاش کنید',
        variant: 'destructive',
      });
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fa-IR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return {
    isLoading,
    users,
    announcements,
    events,
    submissions,
    fetchData,
    handleUpdateUserRole,
    handleUpdateSubmissionStatus,
    formatDate,
  };
};
