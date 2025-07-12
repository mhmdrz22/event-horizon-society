import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import NewsCard from '@/components/common/NewsCard';
import Search from '@/components/ui/search';
import { News } from '@/schemas/news';
import api from '@/services/api';
import { toast } from '@/hooks/use-toast';
import { Skeleton } from '@/components/ui/skeleton';

const NewsPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [allNews, setAllNews] = useState<News[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchNews = async () => {
      setIsLoading(true);
      try {
        const response = await api.get<News[]>('/news/');
        setAllNews(response.data);
      } catch (error) {
        console.error('Error fetching news:', error);
        toast({
          title: 'خطا در بارگذاری اخبار',
          variant: 'destructive',
        });
      } finally {
        setIsLoading(false);
      }
    };
    fetchNews();
  }, []);

  const filteredNews = allNews.filter(newsItem =>
    newsItem.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    newsItem.content.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  return (
    <div className="container py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2 text-navy dark:text-white">اخبار و اطلاعیه‌ها</h1>
        <p className="text-muted-foreground">با آخرین اخبار و اطلاعات از جامعه علمی ما به روز بمانید</p>
      </div>

      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="w-full">
          <Search placeholder="جستجوی اخبار..." onSearch={handleSearch} />
        </div>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, index) => (
            <CardSkeleton key={index} />
          ))}
        </div>
      ) : filteredNews.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredNews.map((newsItem) => (
            <NewsCard key={newsItem.id} newsItem={newsItem} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <h3 className="text-xl font-medium mb-2">هیچ خبری یافت نشد</h3>
          <p className="text-muted-foreground mb-4">معیارهای جستجو خود را تنظیم کنید</p>
          <Button
            variant="outline"
            onClick={() => setSearchQuery('')}
          >
            پاک کردن جستجو
          </Button>
        </div>
      )}
    </div>
  );
};

const CardSkeleton = () => (
    <div className="flex flex-col space-y-3">
        <Skeleton className="h-[125px] w-full rounded-xl" />
        <div className="space-y-2">
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
        </div>
    </div>
)

export default NewsPage;
