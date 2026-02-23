'use client';

import { useState } from 'react';
import { Search } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Button } from '@/components/ui/button';

interface RecipeFiltersProps {
  onFilterChange: (filters: {
    search: string;
    tag: string;
    difficulty: string;
  }) => void;
}

const popularTags = [
  'breakfast',
  'lunch',
  'dinner',
  'dessert',
  'vegetarian',
  'vegan',
  'quick',
  'healthy',
  'comfort-food',
];

export function RecipeFilters({ onFilterChange }: RecipeFiltersProps) {
  const [search, setSearch] = useState('');
  const [tag, setTag] = useState('');
  const [difficulty, setDifficulty] = useState('');

  const handleApplyFilters = () => {
    onFilterChange({ search, tag, difficulty });
  };

  const handleReset = () => {
    setSearch('');
    setTag('');
    setDifficulty('');
    onFilterChange({ search: '', tag: '', difficulty: '' });
  };

  return (
    <div className="bg-card rounded-lg border p-6 shadow-sm space-y-4">
      <div className="space-y-2">
        <Label htmlFor="search">Search Recipes</Label>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            id="search"
            placeholder="Search by title or description..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleApplyFilters();
              }
            }}
            className="pl-9"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="tag">Tag</Label>
          <Select value={tag} onValueChange={setTag}>
            <SelectTrigger id="tag">
              <SelectValue placeholder="All tags" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All tags</SelectItem>
              {popularTags.map((t) => (
                <SelectItem key={t} value={t}>
                  {t}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="difficulty">Difficulty</Label>
          <Select value={difficulty} onValueChange={setDifficulty}>
            <SelectTrigger id="difficulty">
              <SelectValue placeholder="All levels" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All levels</SelectItem>
              <SelectItem value="easy">Easy</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="hard">Hard</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="flex gap-2 pt-2">
        <Button onClick={handleApplyFilters} className="flex-1">
          Apply Filters
        </Button>
        <Button onClick={handleReset} variant="outline">
          Reset
        </Button>
      </div>
    </div>
  );
}
