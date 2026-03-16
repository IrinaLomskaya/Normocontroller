/**
 * ГЛАВНЫЙ LAYOUT ПРИЛОЖЕНИЯ
 * 
 * Этот файл оборачивает все страницы приложения
 * 
 * ЧТО МЕНЯТЬ:
 * - title: название в браузере и закладке
 * - description: описание сайта
 * - favicon и другие метатеги
 */

import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'NormoController - Система расчета нормативов',
  // ИЗМЕНЯЙ: title - это текст в закладке браузера
  description: 'Система размещения и расчета нормативов',
  // ИЗМЕНЯЙ: description - это краткое описание сайта
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      {/* 
        HEAD СЕСИЯ
        ИЗМЕНЯЙ:
        - charset="utf-8" - кодировка (обычно не меняешь)
        - viewport - адаптация под мобильные (обычно не меняешь)
      */}
      <head>
        {/* Favicon - значок в углу браузера */}
        {/* <link rel="icon" href="/favicon.ico" /> */}
      </head>
      <body>
        {/* ОСНОВНОЙ КОНТЕЙНЕР ПРИЛОЖЕНИЯ */}
        <div className="app-container">{children}</div>
      </body>
    </html>
  )
}
