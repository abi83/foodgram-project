const originURL = new URL(window.location);
const originURLParams = originURL.searchParams;
const tagsParamsString = originURLParams.get('tags') ? originURLParams.get('tags') : 'breakfast,lunch,dinner';
const paginationLInks = document.querySelectorAll('.pagination__link')
const tagLinks = document.querySelectorAll('.tags__checkbox')

const tagsObj = {
  breakfast: tagsParamsString.includes('breakfast'),
  lunch: tagsParamsString.includes('lunch'),
  dinner: tagsParamsString.includes('dinner'),
}
function tagsObjToString(tObj) {
    let tags = '';
    for (let tag in tagsObj){
      if (tagsObj[tag]){tags += tag;tags += ',';}
    }
    return tags.slice(0, -1);
}

// remote active class from unselected tags
tagLinks.forEach(item=>{
      if (!tagsObj[item.id]){
        item.classList.remove('tags__checkbox_active')
      }
})

//redirect to correct page on tag click
tagLinks.forEach(item=>item
  .addEventListener('click', event => {
    originURLParams.delete('tags');
    tagsObj[event.target.id] = !tagsObj[event.target.id];
    originURLParams.append('tags', tagsObjToString(tagsObj))
    window.location.href = ('?' + originURLParams.toString()).toString();
}));

// adding current url params to all paginator links
paginationLInks.forEach((link)=> {
    let url = new URL(link.href);
    let params = url.searchParams;
    params.append('tags', tagsObjToString(tagsObj));
    link.href = ('?' + params.toString()).toString()
  })