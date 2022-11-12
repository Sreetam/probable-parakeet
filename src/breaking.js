import React from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import Carousel from 'react-bootstrap/Carousel';

export default function Breaking(content) {
  const contentLength = 150;
  return (
    <div className="container">
      <div className="row">
        <div className="col-6">
          <Carousel fade variant="dark" style={{ width: '100%', height: '200px' }}>
            {content.slice(0,content.length/2).map((news) => (
                <Carousel.Item>
                  <img
                    className="breaking-img"
                    src={news[4]}
                    alt=""
                  />
                  <Carousel.Caption>
                    <h5>{news[2]}</h5>
                    <p>
                      {news[3].substring(0,contentLength)}
                    </p>
                  </Carousel.Caption>
                </Carousel.Item>
            ))}
          </Carousel>
        </div>
      </div>
      <div className="row">
        <div className="col-6">
          <Carousel fade variant="dark" style={{ width: '100%', height: '200px' }}>
            {content.slice(content.length/2).map((news) => (
                <Carousel.Item>
                  <img
                    className="breaking-img"
                    src={news[4]}
                    alt=""
                  />
                  <Carousel.Caption>
                    <h5>{news[2]}</h5>
                    <p>
                      {news[3].substring(0,contentLength)}
                    </p>
                  </Carousel.Caption>
                </Carousel.Item>
            ))}
          </Carousel>
        </div>
      </div>
    </div>
  );
}