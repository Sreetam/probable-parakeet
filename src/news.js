import Card from 'react-bootstrap/Card';
import React, { useEffect, useReducer } from 'react';

const reducer = (state, action) => {
  switch(action) {
    case 2:
      return 2;
    case 0:
      return 1;
    default:
      return 0;
  }
}

function News(news) {
  const [showMore, setShowMore] = useReducer(reducer, 0);
  
  const content = () => {
    return showMore===1 ? news[2] : (news[3].length===0?news[2]:news[3].substring(0,300));
  }
  
  useEffect(() => {
    const intervalRef = setInterval(() => {
      setShowMore(showMore);
    }, 1000);

    return () => {
      clearInterval(intervalRef);
    }
  },[showMore]);

  return (
    <Card style={{ width: '100%', height: '150px' }}>
      <Card.Body className='card-body'
      onMouseEnter={() => setShowMore(2)}
      onMouseLeave={() => setShowMore(0)}
      >
        <Card.Text>{content()}</Card.Text>
      </Card.Body>
    </Card>
  );
}
export default News;