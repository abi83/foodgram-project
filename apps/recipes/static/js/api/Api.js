function getCookieFromDoc(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

class Api {
  constructor(apiUrl) {
      this.apiUrl =  apiUrl;
      this.headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookieFromDoc('csrftoken'),
      }
  }
  getPurchases () {
    return fetch(`/purchases`, {
      headers: this.headers,
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addPurchases (id) {
    return fetch(`/api/v1/cart/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        recipe_slug: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  // TODO: ask what is going on here. Where is catch?
  removePurchases (id){
    return fetch(`/api/v1/cart/${id}`, {
      method: 'DELETE',
      headers: this.headers,
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addSubscriptions(id) {
    return fetch(`/api/v1/subscriptions/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        id: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions (id) {
    return fetch(`/api/v1/subscriptions/${id}`, {
      method: 'DELETE',
      headers: this.headers,
    })
      .then( e => {
          if(e.ok) {
              return e
          }
          return Promise.reject(e.statusText)
      })
  }
  addFavorites (id)  {
    return fetch(`/api/v1/favorites/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        recipe_slug: id
      })
    })
          .then( e => {
            if(e.ok) {
              return e.json()
            }
            return Promise.reject(e.statusText)
          })
  }
  removeFavorites (id) {
    return fetch(`/api/v1/favorites/${id}`, {
      method: 'DELETE',
      headers: this.headers,
    })
      .then( e => {
        if(e.ok) {
          return e
        }
        return Promise.reject(e.statusText)
      })
  }
  getIngredients  (text)  {
    return fetch(`/api/v1/ingredients/?query=${text}`, {
      headers: this.headers,
    })
      .then( e => {
        if(e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
}
