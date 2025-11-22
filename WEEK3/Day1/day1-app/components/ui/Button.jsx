export default function Button({size, type, children,className=""}) {
    const ButtonType = {
    primary: "bg-blue-600 hover:bg-blue-400 text-white font-bold rounded",
    secondary: "bg-yellow-600 hover:bg-yellow-400 text-white font-bold rounded",
    basic: "bg-green-600 hover:bg-green-400 text-white-700 font-bold rounded",
    delete: "bg-red-600 hover:bg-red-400 text-white font-bold rounded",
    other:""
};

    const ButtonSize = {
    sm: "py-2 px-4 text-xs",
    lg: "py-3 px-6 text-lg"
};

  // This can be improved. I’m keeping it simple here by joining two strings.
    const classNames = (ButtonType[type] || ButtonType.other) + " " + (ButtonSize[size] || ButtonSize.sm)+" "+ className;

    return (
    <button className={classNames}>
        {children}
    </button>
    )
}
