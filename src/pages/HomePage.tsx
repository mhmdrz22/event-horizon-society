import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import NewsCard from '@/components/common/NewsCard';
import EventCard from '@/components/common/EventCard';
import { Link } from 'react-router-dom';
import api from '@/services/api';
import { News } from '@/schemas/news';
import { EventResponse } from '@/schemas/event';

const HomePage: React.FC = () => {
  const [latestNews, setLatestNews] = useState<News[]>([]);
  const [upcomingEvents, setUpcomingEvents] = useState<EventResponse[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const newsResponse = await api.get<News[]>('/news/', { params: { limit: 3 } });
        setLatestNews(newsResponse.data);

        const eventsResponse = await api.get<EventResponse[]>('/events/', { params: { limit: 2 } });
        setUpcomingEvents(eventsResponse.data);
      } catch (error) {
        console.error("Error fetching homepage data:", error);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient text-white py-20 px-4">
        <div className="container mx-auto text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
            انجمن علمی دانشگاه
          </h1>
          <p className="text-lg md:text-xl max-w-2xl mx-auto mb-8 opacity-90">
            با دانشمندان دیگر ارتباط برقرار کنید، فرصت‌های پژوهشی را کشف کنید و از آخرین رویدادها و اعلانات علمی مطلع شوید
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/signup">
              <Button className="bg-gold text-black hover:bg-gold/90 text-lg px-8 py-6">
                به جامعه ما بپیوندید
              </Button>
            </Link>
            <Link to="/events">
              <Button variant="outline" className="text-white border-white hover:bg-white/10 text-lg px-8 py-6">
                مشاهده رویدادها
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Announcements Section */}
      <section className="py-16 px-4 bg-background">
        <div className="container mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold">آخرین اخبار</h2>
            <Link to="/news">
              <Button variant="ghost" className="text-gold hover:text-gold">
                مشاهده همه
              </Button>
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {latestNews.map((newsItem) => (
              <NewsCard key={newsItem.id} newsItem={newsItem} />
            ))}
          </div>
        </div>
      </section>

      {/* Events Section */}
      <section className="py-16 px-4 bg-muted">
        <div className="container mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold">رویدادهای پیش رو</h2>
            <Link to="/events">
              <Button variant="ghost" className="text-gold hover:text-gold">
                مشاهده همه
              </Button>
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {upcomingEvents.map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="py-16 px-4 bg-navy text-white">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">آماده مشارکت هستید؟</h2>
          <p className="text-lg max-w-2xl mx-auto mb-8 opacity-90">
            پژوهش، ایده‌ها یا مقالات خود را با جامعه علمی ما به اشتراک بگذارید
          </p>
          <Link to="/submit-article">
            <Button className="bg-gold text-black hover:bg-gold/90 text-lg px-8 py-6">
              ارسال اثر شما
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
