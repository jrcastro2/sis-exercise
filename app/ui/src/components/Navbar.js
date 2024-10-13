import React from 'react';
import { Layout, Menu } from 'antd';
import { Link, useLocation } from 'react-router-dom';

const { Header } = Layout;

const Navbar = () => {
  const location = useLocation();

  return (
    <Header>
      <Link to="/search">
        <div className="logo">
          Exercise
        </div>
      </Link>
      <Menu theme="dark" mode="horizontal" selectedKeys={[location.pathname]}>
        <Menu.Item key="/search">
          <Link to="/search">Search</Link>
        </Menu.Item>
        <Menu.Item key="/stats">
          <Link to="/stats">Stats</Link>
        </Menu.Item>
      </Menu>
    </Header>
  );
};

export default Navbar;