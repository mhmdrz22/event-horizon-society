
import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuth } from '@/contexts/AuthContext';
import { Loader2 } from 'lucide-react';

const ProfilePage: React.FC = () => {
  const { user, loading, updateProfile, signOut } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    student_id: '',
    phone_number: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || '',
        email: user.email || '',
        student_id: user.student_id || '',
        phone_number: user.phone_number || '',
      });
    }
  }, [user]);

  if (loading) {
    return (
      <div className="container py-8 px-4 flex justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-navy" />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="container py-8 px-4 flex justify-center">
        <p>Please log in to view your profile.</p>
      </div>
    );
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await updateProfile({
        full_name: formData.full_name,
        student_id: formData.student_id,
        phone_number: formData.phone_number,
      });
      setIsEditing(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>پروفایل من</CardTitle>
            <CardDescription>
              اطلاعات حساب خود را مشاهده و مدیریت کنید
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="role">نقش</Label>
                <Input id="role" value={user.role} disabled />
              </div>
              <div className="space-y-2">
                <Label htmlFor="full_name">نام کامل</Label>
                <Input
                  id="full_name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">ایمیل</Label>
                <Input id="email" value={formData.email} disabled />
              </div>
              <div className="space-y-2">
                <Label htmlFor="student_id">شماره دانشجویی</Label>
                <Input
                  id="student_id"
                  name="student_id"
                  value={formData.student_id}
                  onChange={handleChange}
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone_number">شماره تلفن</Label>
                <Input
                  id="phone_number"
                  name="phone_number"
                  value={formData.phone_number}
                  onChange={handleChange}
                  disabled={!isEditing}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="created">عضویت از</Label>
                <Input
                  id="created"
                  value={new Date(user.created_at).toLocaleDateString('fa-IR')}
                  disabled
                />
              </div>
            </CardContent>
            <CardFooter className="flex flex-col sm:flex-row-reverse gap-4">
              {isEditing ? (
                <>
                  <Button 
                    type="submit" 
                    disabled={isSubmitting}
                    className="w-full sm:w-auto"
                  >
                    {isSubmitting ? 'در حال ذخیره...' : 'ذخیره تغییرات'}
                  </Button>
                  <Button 
                    type="button" 
                    variant="outline" 
                    onClick={() => setIsEditing(false)}
                    className="w-full sm:w-auto"
                    disabled={isSubmitting}
                  >
                    لغو
                  </Button>
                </>
              ) : (
                <>
                  <Button 
                    type="button" 
                    onClick={() => setIsEditing(true)}
                    className="w-full sm:w-auto"
                  >
                    ویرایش پروفایل
                  </Button>
                  <Button 
                    type="button" 
                    variant="destructive"
                    onClick={signOut}
                    className="w-full sm:w-auto"
                  >
                    خروج
                  </Button>
                </>
              )}
            </CardFooter>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default ProfilePage;
