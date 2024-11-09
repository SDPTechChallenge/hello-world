"use client";

import HeaderOptions from "./HeaderOptions";

const Header = () => {
  return (
    <>
      <h1 className="text-center text-lg font-bold text-zinc-200">
        Tech Challenge AI
      </h1>
      <div className="flex flex-row gap-4 items-center">
        <HeaderOptions />
      </div>
    </>
  );
};

export default Header;
