import { redirect } from "next/navigation";

const HomePage = () => {
  return redirect("/chat");
};

export default HomePage;
