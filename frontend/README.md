# NormoController Frontend

Фронтенд приложение для системы размещения и расчета нормативов, построенное на **Next.js** и **React**.

## 📋 Требования

- Node.js версия 16.8 или новее
- npm (поставляется с Node.js)

## 🚀 Быстрый старт

### 1️⃣ Установка зависимостей

```bash
npm install
```

### 2️⃣ Запуск в режиме разработки

```bash
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

### 3️⃣ Построение для продакшена

```bash
npm run build
npm start
```

## 📁 Структура проекта

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx      ← Главный layout (шапка, footer и т.д.)
│   │   ├── page.tsx        ← Главная страница (собирает все компоненты)
│   │   └── globals.css     ← Глобальные стили (ОЧЕНЬ МНОГО КОММЕНТАРИЕВ!)
│   ├── components/
│   │   ├── Header.tsx      ← Шапка приложения
│   │   └── Controller.tsx  ← Кнопки и окно результатов
│   └── (может быть больше компонентов)
├── package.json            ← Зависимости проекта
├── tsconfig.json           ← Конфиг TypeScript
├── next.config.js          ← Конфиг Next.js
└── README.md               ← Этот файл
```

## 🎨 Что менять

### 🔴 Цвета кнопок и шапки

Открой [src/app/globals.css](src/app/globals.css) и найди:
- `.header` - стили шапки
- `.button-upload` - кнопка "Загрузить документы" (розовая)
- `.button-calculate` - кнопка "Рассчитать ответ" (голубая)
- `.button-vector` - кнопка "Загрузить в хранилище" (розовая)
- `.button-clear` - кнопка "Очистить хранилище" (жёлтая)

Поменяй значения `background` с hex-кодов на свои цвета.

### 📝 Текст

- Шапка: [src/components/Header.tsx](src/components/Header.tsx)
- Кнопки: [src/components/Controller.tsx](src/components/Controller.tsx) - ищи строки с 📄 и 🧮

### 🔌 Подключение бэкенда

В файле [src/components/Controller.tsx](src/components/Controller.tsx) найди комментарии:
- `ДЕМО РЕЖИМ` ← сейчас приложение работает в демо режиме
- `ВОТ ЗДЕСЬ ОТПРАВЛЯЙ ЗАПРОС` ← раскомментируй код для подключения к бэкенду

Замени endpoints `/api/upload` и `/api/calculate` на реальные адреса твоего сервера.

### 🎯 Размер окна результатов

В [src/app/globals.css](src/app/globals.css) найди `.results-window`:
```css
min-height: 300px;  ← Измени это число на нужный размер
```

## 💡 Как разворачиваться

### Добавить новую кнопку

1. Открой [src/components/Controller.tsx](src/components/Controller.tsx)
2. Добавь новую функцию перед кнопками:
```typescript
const handleNewAction = () => {
  // Твой код здесь
}
```

3. Добавь кнопку в JSX:
```tsx
<button className="button" style={{ background: 'linear-gradient(135deg, #цвет1 0%, #цвет2 100%)' }} onClick={handleNewAction}>
  🎯 Названи кнопки
</button>
```

4. Добавь стили в [src/app/globals.css](src/app/globals.css)

### Добавить новый компонент

1. Создай файл `src/components/MoyComponent.tsx`
2. Напиши компонент
3. Импортируй его в [src/app/page.tsx](src/app/page.tsx)
4. Добавь в layout

### Подключить CSS Framework (Tailwind, Bootstrap и т.д.)

Если хочешь использовать Tailwind CSS вместо обычного CSS:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Потом добавь в `.button` и другие классы `@apply` директивы.

## 🐛 Отладка

### Видно ошибки в консоли браузера?

Открой DevTools (F12) → Console и внимательно прочитай ошибку.

### Файл не загружается?

Проверь в коде [src/components/Controller.tsx](src/components/Controller.tsx) что `accept` параметр соответствует типам файлов которые нужны.

### Стили не применяются?

1. Проверь что класс правильно написан
2. Очисти cache браузера (ctrl+shift+delete)
3. Перезагрузи страницу

## 🌐 Развёртывание

### На Vercel (рекомендуется для Next.js)

1. Закомитай проект в GitHub
2. Иди на [vercel.com](https://vercel.com)
3. Импортируй репозиторий
4. Deploy готов!

### На своём сервере

```bash
npm run build
npm start
```

Сервер запустится на порту 3000 (можно менять через переменные окружения).

## 📚 Полезные ссылки

- [Next.js документация](https://nextjs.org/docs)
- [React документация](https://react.dev)
- [JavaScript/TypeScript](https://www.typescriptlang.org/docs/)
- [CSS Grid и Flexbox](https://css-tricks.com/)

## 🤝 Совместная разработка

Каждый компонент содержит комментарии `// ИЗМЕНЯЙ:` - это места где можно кастомизировать внешний вид и поведение.

Не меняй логику если не уверен что понимаешь что она делает!

## 📞 Помощь

Если что-то не работает - сначала проверь консоль браузера (F12), там обычно написана суть проблемы.

---

**Успехов в разработке! 🚀**
