import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, Bell, BellOff, CheckCircle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import api from '@/services/api';

interface Notification {
  id: number;
  message: string;
  created_at: string;
  is_read: boolean;
  user_id: number;
}

const NotificationsPage: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  const fetchNotifications = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    try {
      const response = await api.get<Notification[]>('/notifications/');
      setNotifications(response.data || []);
    } catch (error) {
      console.error('Error fetching notifications:', error);
      toast({
        title: 'خطا در دریافت اعلان‌ها',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  const markAsRead = async (notificationId: number) => {
    try {
      await api.put(`/notifications/${notificationId}`);
      setNotifications(prev =>
        prev.map(n => n.id === notificationId ? { ...n, is_read: true } : n)
      );
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      await api.post('/notifications/mark-all-as-read');
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
      toast({ title: 'همه اعلان‌ها خوانده شدند' });
    } catch (error) {
      console.error('Error marking all notifications as read:', error);
    }
  };

  const formatDate = (dateString: string) => {
    return new Intl.DateTimeFormat('fa-IR', {
      year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
    }).format(new Date(dateString));
  };

  if (loading) {
    return (
      <div className="container py-8 px-4 flex justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="container py-8 px-4">
      <div className="mb-8 flex justify-between items-center">
        <h1 className="text-3xl font-bold">اعلان‌ها</h1>
        {notifications.some(n => !n.is_read) && (
          <Button variant="outline" onClick={markAllAsRead}>
            <CheckCircle size={16} className="ml-2" />
            علامت‌گذاری همه به عنوان خوانده شده
          </Button>
        )}
      </div>

      {notifications.length > 0 ? (
        <div className="space-y-4">
          {notifications.map((notification) => (
            <Card key={notification.id} className={!notification.is_read ? 'border-gold' : ''}>
              <CardHeader>
                <div className="flex justify-between">
                  <CardTitle className="flex items-center">
                    <Bell className="ml-2" /> اعلان
                  </CardTitle>
                  {!notification.is_read && (
                    <Button variant="ghost" size="sm" onClick={() => markAsRead(notification.id)}>
                      خواندم
                    </Button>
                  )}
                </div>
                <CardDescription>{formatDate(notification.created_at)}</CardDescription>
              </CardHeader>
              <CardContent>
                <p>{notification.message}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <BellOff className="h-12 w-12 mx-auto text-muted-foreground" />
          <h3 className="mt-4 text-xl font-semibold">اعلانی وجود ندارد</h3>
        </div>
      )}
    </div>
  );
};

export default NotificationsPage;
