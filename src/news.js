import Carousel from 'react-bootstrap/Carousel';
import React from 'react';

function News(news) {
  
  const content = () => {
    return news[3].substring(0,300);
  }
  const headline = () => {
    return news[2];
  }

  return (
    <Carousel.Item>
      <img
        className="d-block w-100"
        src=""
        alt=""
      />

      <Carousel.Caption>
        <h3>{headline()}</h3>
        <p>
          {content()}
        </p>
      </Carousel.Caption>
    </Carousel.Item>
  );
}
export default News;