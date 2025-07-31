import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/contexts/AuthContext';
import { Loader2, Upload } from 'lucide-react';
import { toast } from '@/hooks/use-toast';
import api from '@/services/api';

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ACCEPTED_FILE_TYPES = ["application/pdf"];

const formSchema = z.object({
  title: z.string().min(5, { message: 'عنوان باید حداقل ۵ کاراکتر باشد' }),
  content: z.string().min(50, { message: 'چکیده باید حداقل ۵۰ کاراکتر باشد' }),
  file: z
    .instanceof(File, { message: "فایل مقاله الزامی است" })
    .refine((file) => file.size <= MAX_FILE_SIZE, `حداکثر حجم فایل ۵ مگابایت است`)
    .refine(
      (file) => ACCEPTED_FILE_TYPES.includes(file.type),
      "فقط فایل‌های PDF مجاز هستند"
    ),
});

type FormValues = z.infer<typeof formSchema>;

const ArticleSubmissionPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: '',
      content: '',
      file: undefined,
    },
  });

  const onSubmit = async (data: FormValues) => {
    if (!user) {
      toast({
        title: 'خطای دسترسی',
        description: 'برای ارسال مقاله باید ابتدا وارد سیستم شوید',
        variant: 'destructive',
      });
      navigate('/login');
      return;
    }

    setIsSubmitting(true);

    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('content', data.content);
    formData.append('file', data.file);

    try {
      await api.post('/articles/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast({
        title: 'مقاله با موفقیت ارسال شد',
        description: 'مقاله شما برای بررسی به مدیران ارسال شد',
      });
      form.reset();
      // navigate('/profile');
    } catch (error: any) {
      console.error('Error submitting article:', error);
      toast({
        title: 'خطا در ارسال مقاله',
        description: error.response?.data?.detail || 'لطفا دوباره تلاش کنید',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2 text-navy dark:text-white">ارسال مقاله</h1>
        <p className="text-muted-foreground">ایده‌ها و یافته‌های پژوهشی خود را با جامعه علمی به اشتراک بگذارید</p>
      </div>

      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>فرم ارسال مقاله</CardTitle>
          <CardDescription>لطفا اطلاعات مقاله خود را با دقت تکمیل کنید</CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="title"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>عنوان مقاله</FormLabel>
                    <FormControl>
                      <Input placeholder="عنوان مقاله خود را وارد کنید" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="content"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>چکیده مقاله</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="چکیده مقاله خود را وارد کنید"
                        className="min-h-[150px]"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="file"
                render={({ field: { onChange, ...props } }) => (
                  <FormItem>
                    <FormLabel>فایل مقاله (PDF)</FormLabel>
                    <FormControl>
                      <Input
                        type="file"
                        accept="application/pdf"
                        onChange={(e) => {
                          const file = e.target.files?.[0];
                          if (file) {
                            onChange(file);
                          }
                        }}
                        {...props}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button
                type="submit"
                className="w-full bg-gold text-black hover:bg-gold/90"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                    در حال ارسال...
                  </>
                ) : (
                  <>
                    <Upload className="ml-2 h-4 w-4" />
                    ارسال مقاله
                  </>
                )}
              </Button>
            </form>
          </Form>
        </CardContent>
        <CardFooter className="flex justify-center text-sm text-muted-foreground">
          مقاله شما پس از بررسی توسط مدیران انجمن منتشر خواهد شد
        </CardFooter>
      </Card>
    </div>
  );
};

export default ArticleSubmissionPage;
