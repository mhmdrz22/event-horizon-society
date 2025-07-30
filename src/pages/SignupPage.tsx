import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Link, Navigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Loader2 } from 'lucide-react';

const formSchema = z.object({
  full_name: z.string().min(2, 'نام باید حداقل 2 کاراکتر باشد'),
  email: z.string().email('ایمیل وارد شده معتبر نیست'),
  password: z.string().min(8, 'رمز عبور باید حداقل 8 کاراکتر باشد'),
  student_id: z.string().min(1, 'شماره دانشجویی اجباری است').max(50, 'شماره دانشجویی نمی‌تواند بیشتر از 50 کاراکتر باشد'),
  phone_number: z.string().optional(),
});

type FormValues = z.infer<typeof formSchema>;

const SignupPage: React.FC = () => {
  const { signUp, user, loading } = useAuth();
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      full_name: '',
      email: '',
      password: '',
      student_id: '',
      phone_number: '',
    },
  });

  if (user) {
    return <Navigate to="/" replace />;
  }

  const onSubmit = async (data: FormValues) => {
    await signUp(data);
  };

  return (
    <div className="container flex items-center justify-center min-h-[80vh] py-8 px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">ایجاد حساب کاربری</CardTitle>
          <CardDescription className="text-center">
            اطلاعات خود را برای ایجاد حساب کاربری وارد کنید
          </CardDescription>
        </CardHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <CardContent className="space-y-4">
              <FormField
                control={form.control}
                name="student_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>شماره دانشجویی</FormLabel>
                    <FormControl><Input placeholder="شماره دانشجویی" {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="full_name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>نام کامل</FormLabel>
                    <FormControl><Input placeholder="نام و نام خانوادگی" {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>ایمیل</FormLabel>
                    <FormControl><Input type="email" placeholder="your.email@example.com" {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>رمز عبور</FormLabel>
                    <FormControl><Input type="password" {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? <Loader2 className="ml-2 h-4 w-4 animate-spin" /> : 'ایجاد حساب'}
              </Button>
              <div className="text-center text-sm">
                قبلاً حساب کاربری ایجاد کرده‌اید؟{' '}
                <Link to="/login" className="text-gold hover:underline">
                  ورود
                </Link>
              </div>
            </CardFooter>
          </form>
        </Form>
      </Card>
    </div>
  );
};

export default SignupPage;
