
document.addEventListener("DOMContentLoaded", () => {
  let currentLesson = 1; // ← это важно!
  const continueBtn = Array.from(document.querySelectorAll('.enroll-button_2'))
    .find(btn => btn.textContent.trim() === 'Продолжить');

  const courseCards = document.querySelectorAll('.course-card_1');
  const lessonsPanel = document.createElement('div');
  lessonsPanel.className = 'lessons-panel';

  // Основной контент (слева)
  const content = document.createElement('div');
  content.className = 'lesson-content';

  // Правая панель (темы)
  const sidebar = document.createElement('div');
  sidebar.className = 'lessons-sidebar';
  sidebar.innerHTML = `
    <h4>ОГЭ: Теория вероятности</h4>
    <div class="lesson-item active" data-lesson="1">
      1. Что такое вероятность?
      <span class="points">★ 10</span>
    </div>
    <div class="lesson-item" data-lesson="2">
      2. Считаем вероятность: классическая формула
      <span class="points">★ 10</span>
    </div>
    <div class="lesson-item" data-lesson="3">
      3. Практика
      <span class="points">★ 30</span>
    </div>
  `;

  // Пагинация
  const pagination = document.createElement('div');
  pagination.className = 'pagination-controls';
  pagination.innerHTML = `
    <div style="text-align: right; width: 100%;">
      <button class="btn btn-outline-secondary" id="prevPage" style="display:none;">Назад</button>
      <button class="btn btn-outline-primary" id="nextPage">Далее</button>
    </div>
  `;

  // Контент по урокам
 const lessonsData = {
  1: {
    title: "1. Что такое вероятность?",
    html: `
      <div class="lesson-wrapper">
        <ul><li>События, исходы, вероятность.</li></ul>
        <div class="lesson-image-block">
          <img src="img/кубики.png" alt="Кубики" class="styled-image">
        </div>
        <div class="lesson-text-block">
          <p><strong>Случайность:</strong> что это такое? В жизни полно непредсказуемых ситуаций. Случайное событие — это то, что может случиться, а может и нет, при определённом опыте (например, выпал орёл или решка, выигрыш в лотерею или нет).</p>
          <p><strong>Теория вероятностей:</strong> наука о шансах. Это раздел математики, который позволяет нам измерять возможность различных событий. Это как компас в мире неопределённости: помогает принимать обоснованные решения.</p>

          <h6>Ключевые понятия:</h6>
          <ul>
            <li><strong>Испытание</strong> — действие, приводящее к случайному результату (бросок кубика, подбрасывание монеты).</li>
            <li><strong>Исход</strong> — один из возможных результатов (выпал 3, выпал орёл).</li>
            <li><strong>Событие</strong> — любое сочетание исходов (выпало чётное число, выпал орёл и решка).</li>
            <li><strong>Вероятность</strong> — число, показывающее, насколько вероятно наступление события.</li>
          </ul>

          <h6>Важные свойства вероятности:</h6>
          <ul>
            <li>Вероятность всегда от 0 до 1 (или от 0% до 100%).</li>
            <li>Невозможное событие (никогда не произойдёт) имеет вероятность 0.</li>
            <li>Достоверное событие (всегда произойдёт) имеет вероятность 1.</li>
          </ul>

          <h6>Где применяется теория вероятностей?</h6>
          <p>От страхования до прогноза погоды, от медицины до игр! Теория вероятностей лежит в основе всех решений, которые мы принимаем каждый день, оценивая риски, строя прогнозы и принимая оптимальные стратегии.</p>
        </div>
      </div>
    `
  },
    2: {
      title: "2. Считаем вероятность: классическая формула",
      html: `
        <p>P = (благоприятные исходы)/(все исходы)</p>
        <video controls width="100%" style="border-radius: 10px;">
          <source src="video/probability.mp4" type="video/mp4">
          Ваш браузер не поддерживает видео.
        </video>
      `
    },
    3: {
  title: "3. Практика",
  render: renderPracticeFlashcards
}
  };

   function renderLesson(num) {
    const data = lessonsData[num];
    content.innerHTML = `<h5>${data.title}</h5>`;

    if (data.render) {
      data.render(content); // передаём контейнер
    } else {
      const inner = document.createElement("div");
      inner.innerHTML = data.html;
      content.appendChild(inner);
    }

    content.appendChild(pagination);

    const prevBtn = document.getElementById('prevPage');
const nextBtn = document.getElementById('nextPage');

if (num === 3) {
  // Это урок "Практика" — скрываем общие кнопки
  prevBtn.style.display = 'none';
  nextBtn.style.display = 'none';
} else {
  // Показываем кнопки по логике
  prevBtn.style.display = num > 1 ? 'inline-block' : 'none';
  nextBtn.style.display = num < Object.keys(lessonsData).length ? 'inline-block' : 'none';
}

    document.querySelectorAll('.lesson-item').forEach(item => {
      item.classList.toggle('active', item.dataset.lesson == num);
    });
  }

  lessonsPanel.appendChild(content);
  lessonsPanel.appendChild(sidebar);
  document.querySelector('.courses-section').appendChild(lessonsPanel);

  // === Нажатие "Продолжить"
  continueBtn.addEventListener('click', (e) => {
    e.preventDefault();
    document.querySelectorAll('.courses-section h2, .courses-section h3, .courses-section .line')
      .forEach(h => h.style.display = 'none');
    courseCards.forEach(card => card.style.display = 'none');
    lessonsPanel.style.display = 'flex';
    renderLesson(currentLesson);
  });

  // === Клик по боковой панели
  sidebar.addEventListener('click', (e) => {
    if (e.target.closest('.lesson-item')) {
      currentLesson = parseInt(e.target.closest('.lesson-item').dataset.lesson);
      renderLesson(currentLesson);
    }
  });

  // === Кнопки "назад"/"далее"
  pagination.addEventListener('click', (e) => {
    if (e.target.id === 'nextPage' && currentLesson < 3) {
      currentLesson++;
      renderLesson(currentLesson);
    }
    if (e.target.id === 'prevPage' && currentLesson > 1) {
      currentLesson--;
      renderLesson(currentLesson);
    }
  });

  // === Рендер карточек и теста
  function renderPracticeFlashcards(container) {
    let currentCardIndex = 0;
    let testCompleted = false;
    const flashcardsData = [
      { question: "<strong>1.</strong> Что такое вероятность?", answer: "Это числовая мера возможности наступления события." },
      { question: "<strong>2.</strong> Классическая формула вероятности?", answer: "P = m/n, где m — число благоприятных исходов, n — общее число исходов." }
    ];

    const renderCard = () => {
      const card = flashcardsData[currentCardIndex];
      container.innerHTML = `
        <div class="flashcard">
          <div class="flashcard-question">${card.question}</div>
          <div class="flashcard-answer" style="display: none;">${card.answer}</div>
        </div>
        <div class="flashcard-controls">
          <button class="prev-card" ${currentCardIndex === 0 ? 'disabled' : ''}>←</button>
          <button class="show-answer">Показать ответ</button>
          <button class="next-card">→</button>
        </div>
      `;

      container.querySelector(".show-answer").addEventListener("click", () => {
        container.querySelector(".flashcard-answer").style.display = "block";
      });

      container.querySelector(".prev-card").addEventListener("click", () => {
  if (currentCardIndex > 0) {
    currentCardIndex--;
    renderCard();
  } else {
    // если это первый вопрос — выходим из урока 3 и рендерим урок 2
    currentLesson = 2;
    renderLesson(currentLesson);
  }
});

      container.querySelector(".next-card").addEventListener("click", () => {
        currentCardIndex++;
        if (currentCardIndex < flashcardsData.length) {
          renderCard();
        } else {
          renderTestBlock();
        }
      });
    };

    const renderTestBlock = () => {
      container.innerHTML = `
        <div class="quiz-question">
          <p><strong>3.</strong> Невозможное событие (никогда не произойдёт) имеет вероятность...</p>
          <label><input type="radio" name="q1" value="1"> 1</label><br>
          <label><input type="radio" name="q1" value="0"> 0</label><br>
          <label><input type="radio" name="q1" value="0to1"> от 0 до 1</label><br>
          <div id="quiz-feedback" style="margin-top:10px;"></div>
        </div>
        <div class="flashcard-controls">
          <button class="prev-card">← </button>
          <button id="submit-answer" class="btn btn-outline-primary">Завершить</button>
        </div>
      `;

      container.querySelector(".prev-card").addEventListener("click", () => {
        currentCardIndex = flashcardsData.length - 1;
        renderCard();
      });

      container.querySelector("#submit-answer").addEventListener("click", () => {
        const selected = container.querySelector('input[name="q1"]:checked');
        const feedback = container.querySelector("#quiz-feedback");

        if (!selected) {
          feedback.textContent = "Пожалуйста, выберите ответ.";
          feedback.style.color = "orange";
          return;
        }

       if (selected.value === "0") {
      feedback.textContent = "Верно! Невозможное событие имеет вероятность 0.";
      feedback.style.color = "green";

      setTimeout(() => {
        container.innerHTML = `
          <div class="course-completed-message" style="text-align: center; font-size: 24px; margin-top: 50px;">
            ВЫ ЗАВЕРШИЛИ ЭТОТ КУРС!<br>ПОЗДРАВЛЯЕМ!
          </div>
        `;
      }, 800);
    } else {
      feedback.textContent = "Неверно. Попробуйте ещё раз.";
      feedback.style.color = "red";
    }
  });
};

    renderCard();
  }
});
