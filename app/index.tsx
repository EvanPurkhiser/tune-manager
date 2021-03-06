import 'babel-polyfill';

import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router, Route} from 'react-router-dom';
import {css, Global} from '@emotion/react';
import * as Sentry from '@sentry/browser';

import Catalog from 'app/catalog';
import Importer from 'app/importer';

Sentry.init({
  dsn: 'https://208c1692ec594314acbc4e63a3fd775e@sentry.io/1805605',
});

const globalCss = css`
  * {
    box-sizing: border-box;
  }

  ol,
  ul,
  li {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  a:link {
    text-decoration: none;
  }

  :root {
    font-size: 16px;
  }

  body,
  html,
  #root,
  .app {
    margin: 0;
    font-family: 'Roboto Condensed', sans-serif;
    color: #34373a;
    height: 100%;
  }
`;

const AppRouter = _ => (
  <Router>
    <Global styles={globalCss} />
    <Route path="/importer" component={Importer} />
    <Route path="/catalog" component={Catalog} />
  </Router>
);

ReactDOM.render(<AppRouter />, document.getElementById('root'));
