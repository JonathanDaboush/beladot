import React from 'react';

export default function Button({ kind = 'primary', children, ...props }) {
  const cls = `btn ${kind}`;
  return (
    <button className={cls} {...props}>{children}</button>
  );
}
