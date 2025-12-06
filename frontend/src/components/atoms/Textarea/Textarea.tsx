'use client';

import React, { useId } from 'react';
import { cn } from '@/lib/utils';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export function Textarea({
  label,
  error,
  className,
  id,
  rows = 4,
  ...props
}: TextareaProps) {
  const generatedId = useId();
  const textareaId = id || generatedId;

  return (
    <div className={cn('flex flex-col gap-component', className)}>
      {label && (
        <label
          htmlFor={textareaId}
          className={cn(
            'text-body-regular',
            'font-regular',
            'text-text-primary',
            error && 'text-accent-red'
          )}
        >
          {label}
        </label>
      )}
      <textarea
        id={textareaId}
        rows={rows}
        className={cn(
          'w-full',
          'px-component',
          'py-3',
          'rounded-md',
          'bg-background-card',
          'border-2',
          'border-background-glass',
          'text-text-primary',
          'text-body-regular',
          'font-regular',
          'resize-y',
          'transition-all duration-200',
          'focus:outline-none',
          'focus:ring-2',
          'focus:ring-primary',
          'focus:border-primary',
          'focus:ring-offset-2',
          'focus:ring-offset-background-dark',
          'disabled:opacity-50',
          'disabled:cursor-not-allowed',
          'placeholder:text-text-secondary',
          error && 'border-accent-red',
          error && 'focus:ring-accent-red',
          className
        )}
        {...props}
      />
      {error && (
        <span className="text-body-small text-accent-red">
          {error}
        </span>
      )}
    </div>
  );
}

