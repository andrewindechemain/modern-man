import React from 'react';
import Registration from 'pages/Registration'
import renderer from 'react-test-renderer';
describe("registration page",() =>{
  it('renders the registration page', () => {
    const tree = renderer.create(<Registration />).toJSON();
    expect(tree).toMatchSnapshot();
  })
})