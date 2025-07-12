import React from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Link } from 'react-router-dom';
import { News } from '@/schemas/news';

type NewsCardProps = {
  newsItem: News;
};

const NewsCard: React.FC<NewsCardProps> = ({ newsItem }) => {
  const formattedDate = new Date(newsItem.created_at).toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <Card className="h-full hover:shadow-md transition-shadow overflow-hidden flex flex-col">
      <CardHeader className="pb-3">
        <CardTitle className="text-xl line-clamp-2 text-navy dark:text-white">
          {newsItem.title}
        </CardTitle>
      </CardHeader>
      <CardContent className="pb-4 flex-grow">
        <p className="text-muted-foreground text-sm mb-3">{formattedDate}</p>
        <p className="line-clamp-3 text-sm">{newsItem.content}</p>
      </CardContent>
      <CardFooter className="pt-3 border-t flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Avatar className="h-6 w-6">
            <AvatarFallback>{newsItem.author?.full_name?.charAt(0) || '?'}</AvatarFallback>
          </Avatar>
          <span className="text-xs text-muted-foreground">{newsItem.author?.full_name}</span>
        </div>
        <Link to={`/news/${newsItem.id}`}>
          <Button variant="ghost" size="sm" className="text-gold hover:text-gold hover:bg-gold/10">
            بیشتر بخوانید
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
};

export default NewsCard;
