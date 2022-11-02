// import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import React, { useState } from 'react';

function News(news) {
    const [showMore, setShowMore] = useState(true);
    // var desc = news[3].length>250?news[3].substring(0,250):news[3];
    const desc = news[3].length===0?news[2]:news[3].substring(0,250);
  return (
    <Card style={{ width: 'auto', height: '100px' }}>
      <Card.Body
      onMouseEnter={() => setShowMore(false)}
      onMouseLeave={() => setShowMore(true)}>
        <Card.Title>{showMore ? news[2] : ""}</Card.Title>
        <Card.Text>{showMore ? "" : desc}</Card.Text>
      </Card.Body>
    </Card>
  );
}
export default News;