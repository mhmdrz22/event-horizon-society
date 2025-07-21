
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from '@/hooks/use-toast';
import { useAdminData } from '@/hooks/useAdminData';
import TabContent from '@/components/admin/TabContent';

const AdminPage: React.FC = () => {
  const { user, profile } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('users');
  
  const {
    isLoading,
    users,
    announcements,
    events,
    submissions,
    fetchData,
    handleUpdateUserRole,
    handleUpdateSubmissionStatus,
    formatDate
  } = useAdminData();

  useEffect(() => {
    // Check if user is admin
    if (profile && profile.role !== 'admin') {
      toast({
        title: 'دسترسی محدود',
        description: 'شما اجازه دسترسی به این بخش را ندارید',
        variant: 'destructive',
      });
      navigate('/');
      return;
    }

    fetchData(activeTab);
  }, [profile, activeTab, navigate, fetchData]);

  return (
    <div className="container py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2 text-navy dark:text-white">پنل مدیریت</h1>
        <p className="text-muted-foreground">مدیریت کاربران، اطلاعیه‌ها، رویدادها و مقالات</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="mb-6">
          <TabsTrigger value="users">کاربران</TabsTrigger>
          <TabsTrigger value="announcements">اطلاعیه‌ها</TabsTrigger>
          <TabsTrigger value="events">رویدادها</TabsTrigger>
          <TabsTrigger value="submissions">مقالات</TabsTrigger>
        </TabsList>

        <TabContent
          tab={activeTab as 'users' | 'announcements' | 'events' | 'submissions'}
          isLoading={isLoading}
          users={users}
          announcements={announcements}
          events={events}
          submissions={submissions}
          formatDate={formatDate}
          handleUpdateUserRole={handleUpdateUserRole}
          handleUpdateSubmissionStatus={handleUpdateSubmissionStatus}
        />
      </Tabs>
    </div>
  );
};

export default AdminPage;
