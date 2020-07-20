# Static Management and Vue Sturcture
```js
./static/
├── css
├── img
│   └── jupiter-images
├── js
│   ├── data
│   └── vue
│       ├── app
│       ├── components
│       ├── plugins
│       ├── store
│       └── templates
├── products
└── whatwedo
```
## **`css`**, **`img`** 
directories are self explantory

##  **`js`**
```js
├── js
│   ├── data
│   └── vue
│       ├── app
│       ├── components
│       ├── plugins
│       ├── store
│       └── templates
```
This is main directory in static, responsible overlooks of many website functionalties, that inclueds ...
- razorpay payment scripts
- custom animation
- landing animations
- Vue App
- ... etc


Doc will discussed more on **Vue** part of it. How ***vue app*** is made.
> ### Vue
```js
js
|___
|   |── data
│   └── vue
│       ├── app
│       ├── components
│       ├── plugins
│       ├── store
│       └── templates
```
All logic of vue app making is done in 2 directory **data** and **vue**. Vue is totally loaded from cdn, and so the project structure is adjusted accoridinly if compared from many online docs.
1. **`data`**
    - It contians template for data used by particular ***vue app***. Here *Mercury Product* and *Mercury Data Page*.
    - Its also describes the data classes, and data dictionaries used by vue store[vue-store]
2. **`vue`**
    - Divided into 5 sub folders.
        - app 
            - Main entry point, contains the view root app, 
            - It is directory mounted into html.
        - components
            - Includes all the sub-components need for the app
            - Components are initiated with `Vue.component` function.
            - Components are store in constant with name format X<app-name-camelCase>, e.g. MTableWrapper.
            - Refer components from [Vue][vue-components]
        - plugins
            - Can puts any customs plugins needed for vue
        - store
            - It is store, that stores global state of App.
            - Store has these subdivision
                - State : variables that vue observes for any change
                - Getters: functions that returns state, can do intermidate transformations
                - Mutations : state is only updated in mutation function, can call with `commit` syntax
                - Actions: It also update state through **mutations**. Mainly used for asynchonous loading data(Used [**`axios`**][axios] here)

            - Refer [Vue Store][vue-store]
        - templates
            - It contains templates strings from the each components in `components` folder.
            - Templates are stored in constant as strings with name format X_<app-name-capital-snake-case>, e.g. M_TABLE_WRAPPER
            - Strings may includes any htmls tags, bootsrap classes, or any other style / js function included from main **`.html`**

## Refrences 
- Bootstap 4 : https://getbootstrap.com/docs/4.5/getting-started/introduction/
- JQuery : https://api.jquery.com/
- Axios : https://blog.logrocket.com/how-to-make-http-requests-like-a-pro-with-axios/
- Axios NPM : https://www.npmjs.com/package/axios
- Vue : https://vuejs.org/v2/guide/
- Vue Store : https://vuex.vuejs.org/

[axios]: https://www.npmjs.com/package/axios
[vue]: https://vuejs.org/v2/guide/
[vue-store]: https://vuex.vuejs.org/
[vue-components]: https://vuejs.org/v2/guide/components-registration.html