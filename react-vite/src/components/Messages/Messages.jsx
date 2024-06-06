import { useDispatch, useSelector } from "react-redux";
import { createMessageThunk, getMessagesArray } from "../../redux/messages";
import styles from "./Messages.module.css";
import { useEffect, useState } from "react";
import CreateChannelModal from "../Channels/CreateChannelModal";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import { CiEdit } from "react-icons/ci";
import { thunkGetAll } from "../../redux/session";
import default_user from "../../../../images/default_user.jpg";

function MessagesList() {
  const server = useSelector((state) => state.server.current);
  const channel = useSelector((state) => state.channel.current);
  const messages = useSelector(getMessagesArray);
  const user = useSelector((state) => state.session.user);
  const allUsers = useSelector((state) => state.session);
  const [inputText, setInputText] = useState("");
  const [errors, setErrors] = useState({});
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(thunkGetAll());
  }, [dispatch]);

  if (!server || !channel) return "";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    const message = {
      channel_id: channel.id,
      text: inputText,
    };
    if (!inputText.trim().length) {
      setErrors({ error: "Message Text Required" });
    } else if (inputText.length > 250) {
      setErrors({ error: "Max length: 250" });
    } else {
      await dispatch(createMessageThunk(channel, message));
      setInputText("");
    }
  };

  return (
    <main className={styles.main}>
      <div className={styles.channelHead}>
        <h1>{channel.name}</h1>
        {server?.owner_id === user.id && (
          <OpenModalButton
            className={styles.channel}
            buttonText={
              <>
                Create Channel: <CiEdit />
              </>
            }
            modalComponent={<CreateChannelModal serverId={server.id} />}
          />
        )}
      </div>
      <div className={styles.list}>
        {messages.length > 0 &&
          messages.map((message) => {
            const author = allUsers[message.user_id];
            const src = author.image[0]?.img_url
              ? author.image[0].img_url
              : default_user;
            return (
              <>
                <img className={styles.userImage} src={src} />
                <div>{author.username}</div>
                <div className={styles.message} key={message.id}>
                  {message.text}
                </div>
                {user.id === message.user_id && <button className={styles.delete}>delete</button>}
              </>
            );
          })}

        <form className={styles.form} onSubmit={handleSubmit}>
          <input
            className={styles.input}
            type="text"
            value={inputText}
            placeholder="Type your message here..."
            onChange={(e) => {
              setInputText(e.target.value);
              setErrors({});
            }}
          />
          <button className={styles.submit} type="submit">
            Send Message
          </button>
          <div className={styles.error}>{errors.error && errors.error}</div>
        </form>
      </div>
    </main>
  );
}

export default MessagesList;