import React from "react";

import 'bootstrap/dist/css/bootstrap.css';
import Carousel from 'react-bootstrap/Carousel';

export default function Breaking(content) {

  return (
    <div className="container">
      <div className="row">
        <div className="col-3">
          <Carousel fade style={{ width: '100%', height: '200px' }}>
            {content.slice(0,4).map((news) => (
                <Carousel.Item>
                  <img
                    className="d-block w-100"
                    src=""
                    alt=""
                  />
                  <h5>{news[2]}</h5>
                  <p>
                    {news[3].substring(0,100)}
                  </p>
                </Carousel.Item>
            ))}
          </Carousel>
        </div>
        <div className="col-3">
          <Carousel fade style={{ width: '100%', height: '200px' }}>
            {content.slice(5,9).map((news) => (
                <Carousel.Item>
                  <img
                    className="d-block w-100"
                    src=""
                    alt=""
                  />
                  <h5>{news[2]}</h5>
                  <p>
                    {news[3].substring(0,100)}
                  </p>
                </Carousel.Item>
            ))}
          </Carousel>
        </div>
      </div>
      <div className="row">
        <div className="col-6">
          <Carousel fade style={{ width: '100%', height: '200px' }}>
            {content.slice(9,13).map((news) => (
                <Carousel.Item>
                  <img
                    className="d-block w-100"
                    src=""
                    alt=""
                  />
                  <h5>{news[2]}</h5>
                  <p>
                    {news[3].substring(0,100)}
                  </p>
                </Carousel.Item>
            ))}
          </Carousel>
        </div>
      </div>
    </div>
  );
}