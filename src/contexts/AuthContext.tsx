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
  signUp: (data: Record<string, unknown>) => Promise<void>;
  signIn: (data: { [key: string]: string }) => Promise<void>;
  signOut: () => void;
  updateProfile: (data: Partial<UserProfile>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Define a type for the decoded token
interface DecodedToken extends UserProfile {
  user_id: string;
  sub: string;
  user_role: UserRole;
}

// Helper function to get user from token
const getUserFromToken = (token: string): UserProfile | null => {
  try {
    const decoded: DecodedToken = jwtDecode(token);
    return {
      id: decoded.user_id,
      email: decoded.sub,
      full_name: decoded.full_name,
      role: decoded.user_role,
      created_at: decoded.created_at,
      student_id: decoded.student_id,
      phone_number: decoded.phone_number,
    };
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
        try {
          // Verify token with backend and get fresh user data
          const response = await api.get('/users/me');
          setUser(response.data);
        } catch (error) {
          console.error("Token verification failed:", error);
          localStorage.removeItem('authToken');
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const signUp = async (signUpData: Record<string, unknown>) => {
    try {
      await api.post('/auth/signup', signUpData);
      toast({
        title: 'ثبت نام موفقیت آمیز',
        description: 'حساب شما ایجاد شد. اکنون می توانید وارد شوید.',
      });
      navigate('/login');
    } catch (error) {
      console.error('Unexpected error during sign up:', error);
      const errorMessage =
        error instanceof Error ? error.message : 'خطای غیرمنتظره رخ داده است.';
      toast({
        title: 'خطا در ثبت نام',
        description: errorMessage,
        variant: 'destructive',
      });
    }
  };

  const signIn = async (signInData: { [key: string]: string }) => {
    try {
      const response = await api.post(
        "/auth/login/access-token",
        new URLSearchParams(signInData),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      const { access_token, user: loggedInUser } = response.data;

      if (access_token) {
        localStorage.setItem("authToken", access_token);
        setUser(loggedInUser); // Use the user object from the response

        toast({
          title: "ورود موفقیت آمیز",
          description: "خوش آمدید!",
        });
        navigate("/");
      }
    } catch (error) {
      console.error("Unexpected error during sign in:", error);
      const errorMessage =
        error instanceof Error ? error.message : 'ایمیل یا رمز عبور نامعتبر است.';
      toast({
        title: "خطا در ورود",
        description: errorMessage,
        variant: "destructive",
      });
    }
  };

  const signOut = () => {
    localStorage.removeItem("authToken");
    setUser(null);
    toast({
      title: "خروج موفقیت آمیز",
    });
    navigate("/login");
  };

  const updateProfile = async (updateData: Partial<UserProfile>) => {
    if (!user) return;

    // Filter out unchanged values
    const changedData = Object.entries(updateData).reduce((acc, [key, value]) => {
      if (value !== user[key as keyof UserProfile]) {
        acc[key as keyof UserProfile] = value;
      }
      return acc;
    }, {} as Partial<UserProfile>);

    if (Object.keys(changedData).length === 0) {
      toast({ title: 'No changes to update.' });
      return;
    }

    try {
      const response = await api.put(`/users/me`, changedData);
      const updatedUser = response.data;
      setUser(updatedUser);
      toast({
        title: "پروفایل به‌روزرسانی شد",
      });
    } catch (error) {
      console.error("Unexpected error updating profile:", error);
      const errorMessage =
        error instanceof Error ? error.message : 'خطای غیرمنتظره رخ داده است.';
      toast({
        title: "خطا در به‌روزرسانی",
        description: errorMessage,
        variant: "destructive",
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
