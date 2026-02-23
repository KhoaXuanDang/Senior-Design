'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChefHat, User, LogOut, BookOpen, PlusCircle, Home } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/lib/auth';
import { logout } from '@/lib/api';
import { useRouter } from 'next/navigation';

export function Navbar() {
  const pathname = usePathname();
  const { user, isAuthenticated, setUser } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout();
      setUser(null);
      router.push('/');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2 font-bold text-xl">
            <ChefHat className="h-6 w-6 text-primary" />
            <span>UC Cookbook</span>
          </Link>
          
          <nav className="hidden md:flex items-center gap-6 text-sm">
            <Link
              href="/"
              className={`transition-colors hover:text-foreground/80 flex items-center gap-1.5 ${
                pathname === '/' ? 'text-foreground font-medium' : 'text-foreground/60'
              }`}
            >
              <Home className="h-4 w-4" />
              Browse
            </Link>
            {isAuthenticated && (
              <>
                <Link
                  href="/recipes/contribute"
                  className={`transition-colors hover:text-foreground/80 flex items-center gap-1.5 ${
                    pathname === '/recipes/contribute' ? 'text-foreground font-medium' : 'text-foreground/60'
                  }`}
                >
                  <PlusCircle className="h-4 w-4" />
                  Contribute
                </Link>
                <Link
                  href="/cookbook"
                  className={`transition-colors hover:text-foreground/80 flex items-center gap-1.5 ${
                    pathname === '/cookbook' ? 'text-foreground font-medium' : 'text-foreground/60'
                  }`}
                >
                  <BookOpen className="h-4 w-4" />
                  My Cookbook
                </Link>
              </>
            )}
          </nav>
        </div>

        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <>
              <div className="hidden sm:flex items-center gap-2 text-sm text-muted-foreground">
                <User className="h-4 w-4" />
                <span>{user?.username}</span>
              </div>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link href="/auth/login">
                <Button variant="ghost" size="sm">
                  Login
                </Button>
              </Link>
              <Link href="/auth/register">
                <Button size="sm">
                  Sign Up
                </Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
