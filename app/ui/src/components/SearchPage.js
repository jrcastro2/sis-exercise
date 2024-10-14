import React, { useState } from 'react';
import { Input, Typography, Spin, message, Collapse, Row, Col, Pagination } from 'antd';
import { searchLiterature } from '../api/literatureApi';

const { Title, Paragraph } = Typography;
const { Search } = Input;

function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [limit, setLimit] = useState(10);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);

  const handleSearch = async (page = 1, pageSize = limit) => {
    if (loading) {
      message.warning("Please wait for the current search to finish.");
      return;
    }

    setLoading(true);
    try {
      const offsetValue = (page - 1) * pageSize;
      const data = await searchLiterature(query, pageSize, offsetValue);
      if (data.total === 0) {
        message.warning("No results found for the search term.");
      } else {
        setResults(data.results);
        setSummary(data.summary);
        setTotal(data.total);
        setOffset(offsetValue);
        setLimit(pageSize);
      }
    } catch (error) {
      message.error("There was an error fetching data.");
      console.error("Error during search", error);
    } finally {
      setLoading(false);
    }
  };

  const collapseItems = results.map((item, index) => ({
    key: `${index + 1}`,
    label: item.title,
    children: <p>{item.abstract}</p>,
  }));

  return (
    <div>
      <Row justify="space-between" align="middle">
        <Col>
          <Title level={2}>Literature Search</Title>
        </Col>
      </Row>

      <Search
        placeholder="Enter a search term"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        enterButton
        onSearch={() => handleSearch(1)}
        loading={loading}
      />

      {loading && <Spin className='center margin-top-20' />}

      {!loading && summary && (
        <>
          <Title level={4}>Summary</Title>
          <Paragraph>{summary}</Paragraph>
        </>
      )}

      {!loading && results.length > 0 && (
        <>
          <Title level={4}>Results</Title>
          <Collapse items={collapseItems} />

          <Pagination
            className='justify-center margin-top-20'
            current={offset / limit + 1}
            total={total}
            pageSize={limit}
            onChange={handleSearch}
            showSizeChanger
            pageSizeOptions={['10', '20', '50']}
            onShowSizeChange={handleSearch}
          />
        </>
      )}
    </div>
  );
}

export default SearchPage;