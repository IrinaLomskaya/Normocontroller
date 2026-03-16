/**
 * КОМПОНЕНТ УПРАВЛЕНИЯ (КНОПКИ И РЕЗУЛЬТАТЫ)
 * 
 * ФУНКЦИИ:
 * - handleUpload: обработка загрузки документов
 * - handleCalculate: обработка расчета
 * - displayResults: вывод результатов
 * 
 * ЧТО МЕНЯТЬ:
 * - текст кнопок
 * - поведение при нажатии кнопок
 * - формат вывода результатов
 * 
 * СТИЛИ НАХОДЯТСЯ В: globals.css
 * Ищи .button-panel, .button, .button-upload, .button-calculate, .results-window
 */

'use client'

import { useState, useRef } from 'react'

interface CalculationResult {
  status: string
  data?: unknown
  error?: string
}

export default function Controller() {
  const [uploadedFile, setUploadedFile] = useState<string | null>(null)
  const [results, setResults] = useState<CalculationResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [vectorStorageFiles, setVectorStorageFiles] = useState<string[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)
  const vectorStorageInputRef = useRef<HTMLInputElement>(null)

  /**
   * ОБРАБОТКА ЗАГРУЗКИ ДОКУМЕНТОВ
   * ИЗМЕНЯЙ:
   * - API endpoint (сейчас /api/upload)
   * - обработку ошибок
   * - формат отправки данных
   */
  const handleUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    
    if (!file) return

    setIsLoading(true)
    
    // ВОТ ЗДЕСЬ ОТПРАВЛЯЙ ФАЙЛ НА БЭКЕНД
    // Пример с использованием FormData:
    const formData = new FormData()
    formData.append('file', file)

    // Раскомментируй и отредактируй когда готов подключить бэкенд:
    /*
    fetch('/api/upload', {
      method: 'POST',
      body: formData,
    })
    .then(res => res.json())
    .then(data => {
      setUploadedFile(file.name)
      setResults({ status: 'success', data: `Файл ${file.name} загружен успешно` })
    })
    .catch(err => {
      setResults({ status: 'error', error: 'Ошибка загрузки файла: ' + err.message })
    })
    .finally(() => setIsLoading(false))
    */

    // ДЕМО РЕЖИМ: просто показываем что файл загружен
    setTimeout(() => {
      setUploadedFile(file.name)
      setResults({
        status: 'success',
        data: `✅ Файл "${file.name}" загружен\nРазмер: ${(file.size / 1024).toFixed(2)} КБ\nТип: ${file.type || 'неизвестен'}`,
      })
      setIsLoading(false)
    }, 1000)
  }

  /**
   * ОБРАБОТКА РАСЧЕТА
   * ИЗМЕНЯЙ:
   * - API endpoint (сейчас /api/calculate)
   * - параметры запроса
   * - формат результатов
   */
  const handleCalculate = async () => {
    if (!uploadedFile) {
      setResults({
        status: 'error',
        error: '⚠️ Сначала загрузи документы!',
      })
      return
    }

    setIsLoading(true)

    // ВОТ ЗДЕСЬ ОТПРАВЛЯЙ ЗАПРОС НА РАСЧЕТ
    // Пример с использованием fetch:
    /*
    fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fileName: uploadedFile }),
    })
    .then(res => res.json())
    .then(data => {
      setResults({ status: 'success', data: JSON.stringify(data, null, 2) })
    })
    .catch(err => {
      setResults({ status: 'error', error: 'Ошибка расчета: ' + err.message })
    })
    .finally(() => setIsLoading(false))
    */

    // ДЕМО РЕЖИМ: показываем примерный результат расчета
    setTimeout(() => {
      setResults({
        status: 'success',
        data: `✅ Расчет завершен\n\nЗагруженный файл: ${uploadedFile}\n\nРезультаты:\n- Значение 1: 45.67\n- Значение 2: 123.45\n- Значение 3: 98.76\n\nСтатус: Успешно`,
      })
      setIsLoading(false)
    }, 2000)
  }

  /**
   * ОБРАБОТКА ЗАГРУЗКИ В ВЕКТОРНОЕ ХРАНИЛИЩЕ
   * ИЗМЕНЯЙ:
   * - API endpoint (сейчас /api/upload-to-vector)
   * - логику обработки множества файлов
   */
  const handleUploadToVector = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files

    if (!files || files.length === 0) return

    setIsLoading(true)

    const fileNames = Array.from(files).map((file) => file.name)
    const fileSize = Array.from(files).reduce((sum, file) => sum + file.size, 0)

    // ВОТ ЗДЕСЬ ОТПРАВЛЯЙ ФАЙЛЫ НА БЭКЕНД
    // Пример с использованием FormData для множественной загрузки:
    /*
    const formData = new FormData()
    Array.from(files).forEach((file) => {
      formData.append('files', file)
    })

    fetch('/api/upload-to-vector', {
      method: 'POST',
      body: formData,
    })
    .then(res => res.json())
    .then(data => {
      setVectorStorageFiles([...vectorStorageFiles, ...fileNames])
      setResults({ 
        status: 'success', 
        data: `✅ ${fileNames.length} файл(ов) загружено в векторное хранилище` 
      })
    })
    .catch(err => {
      setResults({ status: 'error', error: 'Ошибка загрузки: ' + err.message })
    })
    .finally(() => setIsLoading(false))
    */

    // ДЕМО РЕЖИМ: показываем что файлы загружены
    setTimeout(() => {
      setVectorStorageFiles([...vectorStorageFiles, ...fileNames])
      setResults({
        status: 'success',
        data: `✅ ${fileNames.length} файл(ов) успешно загружено в векторное хранилище\n\nЗагруженные файлы:\n${fileNames.map((name) => `• ${name}`).join('\n')}\n\nОбщий размер: ${(fileSize / 1024 / 1024).toFixed(2)} МБ\n\nВсего файлов в хранилище: ${vectorStorageFiles.length + fileNames.length}`,
      })
      setIsLoading(false)
    }, 1500)
  }

  /**
   * ОЧИСТКА ВЕКТОРНОГО ХРАНИЛИЩА
   * ИЗМЕНЯЙ:
   * - API endpoint (сейчас /api/clear-vector-storage)
   * - подтверждение перед удалением
   */
  const handleClearStorage = () => {
    if (vectorStorageFiles.length === 0) {
      setResults({
        status: 'error',
        error: '⚠️ Нечего очищать! Хранилище уже пусто.',
      })
      return
    }

    // Добавь подтверждение перед очисткой
    const confirmed = window.confirm(
      `Ты уверена? Это удалит все ${vectorStorageFiles.length} файлов из хранилища!\nЭто действие нельзя отменить.`,
    )

    if (!confirmed) return

    setIsLoading(true)

    // ВОТ ЗДЕСЬ ОТПРАВЛЯЙ ЗАПРОС НА ОЧИСТКУ
    /*
    fetch('/api/clear-vector-storage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })
    .then(res => res.json())
    .then(data => {
      setVectorStorageFiles([])
      setResults({ status: 'success', data: '✅ Векторное хранилище успешно очищено' })
    })
    .catch(err => {
      setResults({ status: 'error', error: 'Ошибка при очистке: ' + err.message })
    })
    .finally(() => setIsLoading(false))
    */

    // ДЕМО РЕЖИМ: просто очищаем список
    setTimeout(() => {
      setVectorStorageFiles([])
      setResults({
        status: 'success',
        data: '✅ Векторное хранилище успешно очищено\n\nВсе файлы удалены.',
      })
      setIsLoading(false)
    }, 1000)
  }

  return (
    <div className="main-content">
      {/* 
        ПАНЕЛЬ С КНОПКАМИ
        ИЗМЕНЯЙ:
        - расстояние между кнопками (gap в CSS)
        - расположение кнопок (flex-direction, flex-wrap)
        - добавь новые кнопки если нужны
      */}
      <div className="button-panel">
        {/* КНОПКА "ЗАГРУЗИТЬ ДОКУМЕНТЫ" */}
        <button
          className="button button-upload"
          onClick={() => fileInputRef.current?.click()}
          disabled={isLoading}
          // ИЗМЕНЯЙ ТЕКСТ КНОПКИ:
          // Вместо "Загрузить документы" введи свой текст
        >
          {isLoading ? (
            <>
              <span className="loading"></span>
              Загрузка...
            </>
          ) : (
            '📄 Загрузить документы'
          )}
        </button>

        {/* КНОПКА "РАССЧИТАТЬ ОТВЕТ" */}
        <button
          className="button button-calculate"
          onClick={handleCalculate}
          disabled={isLoading || !uploadedFile}
          // ИЗМЕНЯЙ ТЕКСТ КНОПКИ:
          // Вместо "Рассчитать ответ" введи свой текст
        >
          {isLoading ? (
            <>
              <span className="loading"></span>
              Расчет...
            </>
          ) : (
            '🧮 Рассчитать ответ'
          )}
        </button>

        {/* КНОПКА "ЗАГРУЗИТЬ В ВЕКТОРНОЕ ХРАНИЛИЩЕ" */}
        <button
          className="button button-vector"
          onClick={() => vectorStorageInputRef.current?.click()}
          disabled={isLoading}
          // ИЗМЕНЯЙ ТЕКСТ КНОПКИ:
          // Вместо "Загрузить в векторное хранилище" введи свой текст
        >
          {isLoading ? (
            <>
              <span className="loading"></span>
              Загрузка...
            </>
          ) : (
            `📦 Хранилище (${vectorStorageFiles.length})`
          )}
        </button>

        {/* КНОПКА "ОЧИСТИТЬ ХРАНИЛИЩЕ" */}
        <button
          className="button button-clear"
          onClick={handleClearStorage}
          disabled={isLoading || vectorStorageFiles.length === 0}
          // ИЗМЕНЯЙ ТЕКСТ КНОПКИ:
          // Вместо "Очистить хранилище" введи свой текст
        >
          {isLoading ? (
            <>
              <span className="loading"></span>
              Удаление...
            </>
          ) : (
            '🗑️ Очистить хранилище'
          )}
        </button>

        {/* 
          ДОБАВЬ ЕЩЕ КНОПКИ ЕЛИ НУЖНЫ
          Пример:
          <button className="button" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }} onClick={() => {}}>
            🔄 Обновить
          </button>
        */}
      </div>

      {/* 
        СКРЫТЫЙ ФАЙЛОВЫЙ ИНПУТ
        Связан с кнопкой "Загрузить документы"
        ref={fileInputRef} - это то же самое, что и id в HTML
      */}
      <input
        ref={fileInputRef}
        type="file"
        className="file-input"
        onChange={handleUpload}
        // ИЗМЕНЯЙ ФОРМАТ ФАЙЛОВ если нужны другие:
        // accept=".pdf,.xlsx,.doc" или любые другие расширения
        accept=".pdf,.xlsx,.xls,.doc,.docx"
        // УДАЛИ accept если хочешь загружать любые файлы
      />

      {/* 
        СКРЫТЫЙ ФАЙЛОВЫЙ ИНПУТ ДЛЯ ВЕКТОРНОГО ХРАНИЛИЩА
        multiple - позволяет выбрать много файлов сразу
        ref={vectorStorageInputRef} - связан с кнопкой "Загрузить в хранилище"
      */}
      <input
        ref={vectorStorageInputRef}
        type="file"
        className="file-input"
        onChange={handleUploadToVector}
        multiple
        // ИЗМЕНЯЙ ФОРМАТ ФАЙЛОВ если нужны другие:
        accept=".pdf,.xlsx,.xls,.doc,.docx,.txt,.jpg,.png"
        // УДАЛИ accept если хочешь загружать любые файлы
      />

      {/* 
        ОКНО РЕЗУЛЬТАТОВ
        ИЗМЕНЯЙ:
        - цвет фона (background-color в CSS)
        - размер (min-height)
        - граница (border)
        - тень (box-shadow)
      */}
      <div className="results-window">
        {results ? (
          <>
            <div className="results-header">
              {results.status === 'success' ? '✅ Результаты' : '❌ Ошибка'}
            </div>
            <div className="results-content">
              {results.status === 'success' ? results.data : results.error}
            </div>
          </>
        ) : (
          <div className="results-empty">
            {uploadedFile
              ? 'Нажми "Рассчитать ответ" чтобы начать расчет'
              : 'Загрузи документы чтобы начать работу'}
          </div>
        )}
      </div>

      {/* 
        ОТЛАДКА (УДАЛИ ПЕРЕД ПУБЛИКАЦИЕЙ)
        Показывает текущее состояние приложения
      */}
      <div style={{ marginTop: '20px', fontSize: '12px', color: '#999' }}>
        {/* 
        Раскомментируй для отладки:
        <pre>
          loadingState: {isLoading}
          uploadedFile: {uploadedFile || 'нет'}
        </pre>
        */}
      </div>
    </div>
  )
}
