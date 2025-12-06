'use client';

import React from 'react';
import { Button } from '@/components/atoms/Button/Button';
import { cn } from '@/lib/utils';

export interface ButtonGroupProps {
  buttons: Array<{
    label: string;
    onClick: () => void;
    variant?: 'default' | 'tag';
    state?: 'active' | 'inactive';
    disabled?: boolean;
  }>;
  className?: string;
}

export function ButtonGroup({ buttons, className }: ButtonGroupProps) {
  return (
    <div className={cn('flex gap-component', className)}>
      {buttons.map((button, index) => (
        <Button
          key={index}
          variant={button.variant}
          state={button.state}
          onClick={button.onClick}
          disabled={button.disabled}
        >
          {button.label}
        </Button>
      ))}
    </div>
  );
}

