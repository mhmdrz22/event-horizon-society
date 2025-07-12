
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/layout/Layout";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import NewsPage from "./pages/NewsPage";
import EventsPage from "./pages/EventsPage";
import ProfilePage from "./pages/ProfilePage";
import UnauthorizedPage from "./pages/UnauthorizedPage";
import NotFound from "./pages/NotFound";
import { AuthProvider } from "./contexts/AuthContext";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import ArticleSubmissionPage from "./pages/ArticleSubmissionPage";
import NewsDetailPage from "./pages/NewsDetailPage";
import EventDetailPage from "./pages/EventDetailPage";
import AdminPage from "./pages/AdminPage";
import NotificationsPage from "./pages/NotificationsPage";
import RTLProvider from "./components/layout/RTLProvider";

const queryClient = new QueryClient();

const AppWithProviders = () => (
  <BrowserRouter>
    <AuthProvider>
      <RTLProvider>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/unauthorized" element={<UnauthorizedPage />} />
            <Route path="/news" element={<NewsPage />} />
            <Route path="/news/:id" element={<NewsDetailPage />} />
            <Route path="/events" element={<EventsPage />} />
            <Route path="/events/:id" element={<EventDetailPage />} />
            
            {/* Protected routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="/submit-article" element={<ArticleSubmissionPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/notifications" element={<NotificationsPage />} />
            </Route>
            
            {/* Admin routes */}
            <Route element={<ProtectedRoute requiredRoles={['admin']} />}>
              <Route path="/admin" element={<AdminPage />} />
            </Route>
            
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
      </RTLProvider>
    </AuthProvider>
  </BrowserRouter>
);

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <AppWithProviders />
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
