(function() {
  const MAX_REVIEWS = 30;

  const clean = value => value?.innerText?.trim() || '';

  const profName = clean(document.querySelector('[class*="NameTitle__Name"]'))
    || clean(document.querySelector('h1'))
    || 'Unknown Professor';

  const school = clean(
    [...document.querySelectorAll('a[href="/school/880"], a[href$="/school/880"]')]
      .find(link => link.innerText.includes('San Francisco State'))
  ) || 'San Francisco State University';

  const overallRating = clean(document.querySelector('[class*="RatingValue__Numerator"]')) || 'N/A';
  const cards = [...document.querySelectorAll('[class*="Rating__RatingBody"]')].slice(0, MAX_REVIEWS);

  if (cards.length === 0) {
    console.log('No review cards found. Make sure you are on a professor RMP page.');
    return;
  }

  const reviews = cards.map(card => {
    const quality = clean(card.querySelector('[class*="CardNumRating__CardNumRatingNumber"]')) || 'N/A';
    const date = clean(card.querySelector('[class*="TimeStamp__StyledTimeStamp"]')) || 'N/A';
    const course = clean(card.querySelector('[class*="RatingHeader__StyledClass"]')) || 'N/A';
    const metaItems = [...card.querySelectorAll('[class*="MetaItem__StyledMetaItem"]')].map(item => item.innerText.trim());
    const grade = metaItems.find(item => item.startsWith('Grade:'))?.replace('Grade:', '').trim() || 'N/A';
    const wouldTake = metaItems.find(item => item.startsWith('Would Take Again:'))?.replace('Would Take Again:', '').trim() || 'N/A';
    const text = clean(card.querySelector('[class*="Comments__StyledComments"]'));
    const tags = [...card.querySelectorAll('[class*="Tag__StyledTag"]')].map(tag => tag.innerText.trim()).join(', ');

    return { quality, date, course, grade, wouldTake, text, tags };
  }).filter(review => review.text.length > 0);

  const header = `## [COURSE: Multiple] [SOURCE: RateMyProfessor] [PROFESSOR: ${profName}] [SCHOOL: ${school}] [OVERALL: ${overallRating}/5]\n\n`;

  const blocks = reviews.map(review =>
`---
**Review** [${review.date}] - Course: ${review.course} | Quality: ${review.quality}/5 | Grade: ${review.grade} | Would Take Again: ${review.wouldTake}
${review.tags ? `Tags: ${review.tags}\n` : ''}> ${review.text}
`).join('\n');

  const output = header + blocks + '\n---';
  console.log(output);
  copy(output);
  console.log(`\nCopied ${reviews.length} reviews for ${profName} to clipboard.`);
})();
