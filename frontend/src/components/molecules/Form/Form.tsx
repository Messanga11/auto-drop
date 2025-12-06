'use client';

import React from 'react';
import { Input } from '@/components/atoms/Input/Input';
import { Label } from '@/components/atoms/Label/Label';
import { Button } from '@/components/atoms/Button/Button';
import { cn } from '@/lib/utils';

export interface FormProps {
  onSubmit: (data: Record<string, any>) => void;
  children?: React.ReactNode;
  className?: string;
}

export function Form({ onSubmit, children, className }: FormProps) {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data: Record<string, any> = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });
    onSubmit(data);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={cn('flex flex-col gap-card', className)}
    >
      {children}
    </form>
  );
}

// Export form components for convenience
Form.Input = Input;
Form.Label = Label;
Form.Button = Button;

