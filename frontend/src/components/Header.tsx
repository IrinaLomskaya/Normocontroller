/**
 * КОМПОНЕНТ HEADER (ШАПКА)
 * 
 * ЧТО МЕНЯТЬ:
 * - текст h1: "NormoController"
 * - текст p: "Система расчета"
 * - логотип/иконка
 * 
 * СТИЛИ НАХОДЯТСЯ В: globals.css
 * Ищи .header, .header h1, .header p
 */

export default function Header() {
  return (
    <header className="header">
      {/* 
        ЛОГОТИП ИЛИ ИКОНКА
        Раскомментируй и добавь свой логотип если нужно:
        <img src="/logo.png" alt="logo" style={{ width: '40px', marginRight: '15px' }} />
      */}
      <div>
        <h1>НормИС</h1>
        {/* ИЗМЕНИ ТЕКСТ: изменяй текст между <p> и </p> */}
        <p>Нормативная интеллектуальная система</p>
      </div>
    </header>
  )
}
