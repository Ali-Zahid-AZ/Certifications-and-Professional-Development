const filterButtons = document.querySelectorAll('.filter-btn');
const tiles = document.querySelectorAll('.tile');

filterButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const skill = btn.getAttribute('data-skill');
    tiles.forEach(tile => {
      if (skill === 'all' || tile.dataset.skills.includes(skill)) {
        tile.style.display = 'block';
      } else {
        tile.style.display = 'none';
      }
    });
  });
});
