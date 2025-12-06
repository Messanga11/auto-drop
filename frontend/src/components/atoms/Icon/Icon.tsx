'use client';

import React from 'react';
import { tokens } from '@/design-system/tokens';
import { cn } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

export interface IconProps {
  icon: LucideIcon;
  size?: number;
  className?: string;
  strokeWidth?: number;
}

export function Icon({
  icon: IconComponent,
  size = 24,
  className,
  strokeWidth,
}: IconProps) {
  // Use design system values: strokeWidth 1.7px, color #FFFFFF
  const defaultStrokeWidth = tokens.navbar.iconStyle.stroke || 1.7;

  return (
    <IconComponent
      size={size}
      strokeWidth={strokeWidth || defaultStrokeWidth}
      className={cn(className)}
    />
  );
}

