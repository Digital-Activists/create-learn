
  // Добавление варианта ответа при клике на "+ Добавить вариант"
  document.querySelectorAll('.add-variant').forEach(elem => {
    elem.addEventListener('click', () => {
      const label = document.createElement('label');
      const input = document.createElement('input');
      input.type = 'checkbox';
      label.appendChild(input);
      label.appendChild(document.createTextNode(' Новый вариант'));
      elem.parentNode.insertBefore(label, elem);
    });
  });

  // Удаление вопроса или термина
  document.querySelectorAll('.close-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.question, .term').remove();
    });
  });


document.querySelector('.btn.term').addEventListener('click', () => {
  const container = document.createElement('div');
  container.className = 'term';
  container.innerHTML = `
    <div class="term-header">
      <div class="question-number">Новый</div>
      <button class="close-btn" aria-label="Удалить термин">&times;</button>
    </div>
    <input type="text" placeholder="Термин" />
    <textarea rows="4" placeholder="Определение"></textarea>
  `;

  const buttons = document.querySelector('.buttons');
  if (buttons && buttons.parentNode) {
    buttons.parentNode.insertBefore(container, buttons);
  } else {
    console.error('Элемент .buttons или его родитель не найден');
  }
});


document.querySelector('.btn.test').addEventListener('click', () => {
  const container = document.createElement('div');
  container.className = 'question';
  container.innerHTML = `
    <div class="question-header">
      <div class="question-number">Новый</div>
      <div class="score">☆ 0 балл ✎</div>
      <button class="close-btn" aria-label="Удалить вопрос">&times;</button>
    </div>
    <input type="text" placeholder="Вопрос" />
    <div class="answers">
      <label><input type="checkbox" /> Вариант 1</label>
      <label class="add-variant">+ Добавить вариант</label>
    </div>
  `;

  const buttons = document.querySelector('.buttons');
  if (buttons && buttons.parentNode) {
    buttons.parentNode.insertBefore(container, buttons);
  } else {
    console.error('Элемент .buttons или его родитель не найден');
  }
});
