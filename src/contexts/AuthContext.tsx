import { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '@/services/api';
import { toast } from '@/hooks/use-toast';
import { jwtDecode } from 'jwt-decode';

export type UserRole = 'student' | 'member' | 'admin';

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  created_at: string;
  student_id?: string;
  phone_number?: string;
}

interface AuthContextType {
  user: UserProfile | null;
  loading: boolean;
  signUp: (data: any) => Promise<void>;
  signIn: (data: { [key: string]: string; }) => Promise<void>;
  signOut: () => void;
  updateProfile: (data: Partial<UserProfile>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Helper function to get user from token
const getUserFromToken = (token: string): UserProfile | null => {
  try {
    // Assuming the token payload has the user profile structure
    const decoded: UserProfile = jwtDecode(token);
    return decoded;
  } catch (error) {
    console.error("Invalid token:", error);
    return null;
  }
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('authToken');
      if (token) {
        const userFromToken = getUserFromToken(token);
        if (userFromToken) {
          setUser(userFromToken);
          // Optionally, you could verify the token with the backend here
          // For example, by fetching the user profile
          // await fetchUserProfile();
        } else {
          // If token is invalid, remove it
          localStorage.removeItem('authToken');
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const signUp = async (signUpData: any) => {
    try {
      await api.post('/auth/signup', signUpData);
      toast({
        title: 'ثبت نام موفقیت آمیز',
        description: 'حساب شما ایجاد شد. اکنون می توانید وارد شوید.',
      });
      navigate('/login');
    } catch (error: any) {
      console.error('Unexpected error during sign up:', error);
      toast({
        title: 'خطا در ثبت نام',
        description: error.response?.data?.detail || 'خطای غیرمنتظره رخ داده است.',
        variant: 'destructive',
      });
    }
  };

  const signIn = async (signInData: { [key: string]: string; }) => {
    try {
      const response = await api.post('/auth/login/access-token', new URLSearchParams(signInData));
      const { access_token } = response.data;

      if (access_token) {
        localStorage.setItem('authToken', access_token);
        const userFromToken = getUserFromToken(access_token);
        setUser(userFromToken);

        toast({
          title: 'ورود موفقیت آمیز',
          description: 'خوش آمدید!',
        });
        navigate('/');
      }
    } catch (error: any) {
      console.error('Unexpected error during sign in:', error);
      toast({
        title: 'خطا در ورود',
        description: error.response?.data?.detail || 'ایمیل یا رمز عبور نامعتبر است.',
        variant: 'destructive',
      });
    }
  };

  const signOut = () => {
    localStorage.removeItem('authToken');
    setUser(null);
    toast({
      title: 'خروج موفقیت آمیز',
    });
    navigate('/login');
  };

  const updateProfile = async (updateData: Partial<UserProfile>) => {
    if (!user) return;
    try {
      const response = await api.put(`/users/me`, updateData);
      const updatedUser = response.data;
      setUser(updatedUser); // Update user state with the response from the server
      toast({
        title: 'پروفایل به‌روزرسانی شد',
      });
    } catch (error: any) {
      console.error('Unexpected error updating profile:', error);
      toast({
        title: 'خطا در به‌روزرسانی',
        description: error.response?.data?.detail || 'خطای غیرمنتظره رخ داده است.',
        variant: 'destructive',
      });
    }
  };


  const value = {
    user,
    loading,
    signUp,
    signIn,
    signOut,
    updateProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
