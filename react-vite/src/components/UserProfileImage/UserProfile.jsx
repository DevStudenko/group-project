import { useSelector } from 'react-redux';
import UserProfileImageUpload from './UserProfileUpload';
import default_user from "../../../../images/default_user.jpg"

import styles from './UserProfile.module.css'

const UserProfile = () => {
    const user = useSelector((state) => state.session.user);
    return (
      <div className={styles.profileCard}>
      <img
        className={styles.profileImage}
        src={user.image_url || default_user}
        alt={`${user.username}'s profile`}
      />
      <div className={styles.profileDetails}>
        <h1 className={styles.profileTitle}>{user.username}</h1>
        <p className={styles.userInfo}>{user.email}</p>
        <UserProfileImageUpload className={styles.button}/>
      </div>
    </div>

    );
  };

  export default UserProfile
