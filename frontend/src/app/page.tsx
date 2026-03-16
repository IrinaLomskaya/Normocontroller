/**
 * ГЛАВНАЯ СТРАНИЦА ПРИЛОЖЕНИЯ
 * 
 * Содержит:
 * - Header (шапка)
 * - Controller (кнопки и результаты)
 * 
 * ЧТО МЕНЯТЬ:
 * - импорты компонентов
 * - добавление новых компонентов
 * - структуру layout'а
 */

import Header from '@/components/Header'
import Controller from '@/components/Controller'

export default function Home() {
  return (
    <>
      {/* ШАПКА ПРИЛОЖЕНИЯ */}
      <Header />

      {/* ОСНОВНОЙ КОНТЕНТ С КНОПКАМИ И РЕЗУЛЬТАТАМИ */}
      <Controller />

      {/* 
        ДОБАВЬ НОВЫЕ КОМПОНЕНТЫ ЗДЕСЬ если нужны
        Пример:
        <Footer />
        <Sidebar />
      */}
    </>
  )
}
