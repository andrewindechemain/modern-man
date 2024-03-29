import React from "react";
import NotificationBar from '../src/components/NotificationBar';
import SearchBar from '../src/components/SearchBar';
import NavButtons from '../src/components/NavButtons';
import tuxedo1 from '../src/images/tuxedo1.jpg'
import tuxedo2 from '../src/images/white tux stripes.jpg'
import tuxedo3 from '../src/images/Blue Tux.jpg'
import tuxedo4 from '../src/images/tuxedo4.jpg'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar} from '@fortawesome/free-solid-svg-icons'; 

const Searchpage = () => {
    return (
    <>
        <NotificationBar />
        <NavButtons />
        <SearchBar />
        <h4 className="searchresultstitle">Suits and Tuxedos</h4>
        <div className="searchresultsimages">
        <span className="image">
        <div className="container"><span class="ondiscount">-18%</span>
        <img src={tuxedo4} alt="Italian Suits" />
        <p>Black Italian Tuxedo</p>
        {[...Array(4)].map((_, index) => (
        <FontAwesomeIcon key={index} icon={faStar} className="shopping" />
    ))}
        <p id="price">$1000</p>
    </div>
    </span>
    <span className="image">
    <div className="container">
    <span class="onsale">New</span>
        <img src={tuxedo4} alt="Grey Suit" />
        <p>Grey Official Suit</p>
        {[...Array(4)].map((_, index) => (
        <FontAwesomeIcon key={index} icon={faStar} className="shopping" />
    ))}
        <p id="price">$700</p>
        </div>
        </span>
    <span className="image">
        <div className="container">
        <span class="ondiscount">-18%</span>
            <img src={tuxedo4} alt="Blue Tuxedo" />
        <p>Blue Official Tuxedo</p>
        {[...Array(4)].map((_, index) => (
        <FontAwesomeIcon key={index} icon={faStar} className="shopping" />
    ))}
    <p id="price">$1000</p>
    </div>
    </span>
    <span className="image">
    <div className="container">
      <span class="onsale">New</span>
        <img src={tuxedo4} alt="White Suit" />
        <p>White Official Suit</p>
        {[...Array(4)].map((_, index) => (
        <FontAwesomeIcon key={index} icon={faStar} className="shopping" />
    ))}
    <p id="price">$700</p>
    </div>
    </span>
</div>
    </>
    )         
}

export default Searchpage;