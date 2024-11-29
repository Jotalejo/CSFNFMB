import { Link as MuiLink } from "@mui/material";
import { Link as ReactRouterLink } from "react-router";

const Link = (props) => {
  return (
    <MuiLink {...props} component={ReactRouterLink} to={props.href ?? "#"} />
  );
};

export default Link;