import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Calendar, MapPin, Users } from 'lucide-react';
import { toast } from '@/hooks/use-toast';
import { useAuth } from '@/contexts/AuthContext';
import CommentSection from '@/components/common/CommentSection';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import api from '@/services/api';
import { EventResponse } from '@/schemas/event';

const EventDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [event, setEvent] = useState<EventResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRegistering, setIsRegistering] = useState(false);

  const fetchEvent = useCallback(async () => {
    if (!id) return;
    setIsLoading(true);
    try {
      const response = await api.get<EventResponse>(`/events/${id}`);
      setEvent(response.data);
    } catch (error) {
      console.error('Error fetching event:', error);
      toast({
        title: 'خطا در بارگذاری رویداد',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchEvent();
  }, [fetchEvent]);

  const handleRegistration = async () => {
    if (!user) {
      toast({
        title: 'ثبت‌نام نیاز به ورود دارد',
        description: 'لطفا ابتدا وارد حساب کاربری خود شوید',
      });
      navigate('/login');
      return;
    }
    if (!event) return;

    setIsRegistering(true);
    try {
      if (event.is_registered) {
        await api.delete(`/events/${event.id}/unregister`);
        toast({ title: 'ثبت‌نام لغو شد' });
      } else {
        await api.post(`/events/${event.id}/register`);
        toast({ title: 'ثبت‌نام انجام شد' });
      }
      // Refetch event data to update the state
      fetchEvent();
    } catch (error: any) {
      console.error('Error during registration:', error);
      toast({
        title: 'خطا',
        description: error.response?.data?.detail || 'لطفا دوباره تلاش کنید',
        variant: 'destructive',
      });
    } finally {
      setIsRegistering(false);
    }
  };

  if (isLoading) {
    // Skeleton Loader
    return <div>...</div>;
  }

  if (!event) {
    return (
      <div className="container py-8 px-4 text-center">
        <h1 className="text-3xl font-bold mb-4">رویداد یافت نشد</h1>
        <Link to="/events"><Button>بازگشت به لیست رویدادها</Button></Link>
      </div>
    );
  }

  const eventDate = new Date(event.event_datetime);
  const formattedDate = eventDate.toLocaleDateString('fa-IR', { year: 'numeric', month: 'long', day: 'numeric' });
  const formattedTime = eventDate.toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' });
  const registrationPercentage = (event.registered_count / event.capacity) * 100;
  const isFull = event.registered_count >= event.capacity;
  const isPast = new Date(event.event_datetime) < new Date();

  return (
    <div className="container py-8 px-4">
      <div className="mb-6">
        <Link to="/events" className="text-gold hover:underline">بازگشت به لیست رویدادها</Link>
        <h1 className="text-3xl font-bold mt-2">{event.title}</h1>
        <div className="flex flex-wrap gap-2 my-4">
            {isPast ? <Badge variant="secondary">برگزار شده</Badge> : isFull ? <Badge variant="destructive">ظرفیت تکمیل</Badge> : <Badge className="bg-gold text-black">ثبت‌نام فعال</Badge>}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader><CardTitle>درباره این رویداد</CardTitle></CardHeader>
            <CardContent><p>{event.description}</p></CardContent>
          </Card>
          <CommentSection contentType="event" contentId={event.id} />
        </div>
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>ثبت‌نام</CardTitle>
              <CardDescription>{isPast ? 'رویداد به پایان رسیده' : 'در این رویداد شرکت کنید'}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="flex items-center"><Calendar className="ml-2" /><span>{formattedDate} - ساعت {formattedTime}</span></div>
                <div className="flex items-center"><MapPin className="ml-2" /><span>{event.location}</span></div>
                <div className="flex items-center"><Users className="ml-2" /><span>{event.registered_count} از {event.capacity} نفر</span></div>
                <Progress value={registrationPercentage} />
                <Button
                    className="w-full"
                    onClick={handleRegistration}
                    disabled={isRegistering || isPast || (!event.is_registered && isFull)}
                >
                    {isRegistering ? '...' : event.is_registered ? 'لغو ثبت‌نام' : 'ثبت‌نام'}
                </Button>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>برگزار کننده</CardTitle></CardHeader>
            <CardContent>{event.organizer?.full_name || 'انجمن علمی'}</CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default EventDetailPage;
