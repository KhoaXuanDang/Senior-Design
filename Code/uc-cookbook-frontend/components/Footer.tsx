import { ChefHat, Github, Mail } from 'lucide-react';
import Link from 'next/link';

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t bg-muted/40 mt-auto">
      <div className="container py-8 md:py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <ChefHat className="h-5 w-5 text-primary" />
              <span className="font-bold text-lg">UC Cookbook</span>
            </div>
            <p className="text-sm text-muted-foreground">
              A community-driven recipe platform for University of Cincinnati students to share and discover delicious recipes.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold mb-3">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/" className="text-muted-foreground hover:text-foreground transition-colors">
                  Browse Recipes
                </Link>
              </li>
              <li>
                <Link href="/recipes/contribute" className="text-muted-foreground hover:text-foreground transition-colors">
                  Contribute Recipe
                </Link>
              </li>
              <li>
                <Link href="/cookbook" className="text-muted-foreground hover:text-foreground transition-colors">
                  My Cookbook
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-3">Connect</h3>
            <div className="flex gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                <Github className="h-5 w-5" />
                <span className="sr-only">GitHub</span>
              </a>
              <a
                href="mailto:support@uccookbook.com"
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                <Mail className="h-5 w-5" />
                <span className="sr-only">Email</span>
              </a>
            </div>
          </div>
        </div>
        
        <div className="mt-8 pt-6 border-t text-center text-sm text-muted-foreground">
          <p>&copy; {currentYear} UC Cookbook. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
