export default function Button({size, type, children}) {
    const ButtonType = {
    primary: "bg-blue-500 hover:bg-blue-700 text-white font-bold rounded",
    secondary: "bg-blue-500 hover:bg-blue-700 text-white font-bold rounded",
    basic: "bg-white hover:bg-gray-700 text-gray-700 font-bold rounded",
    delete: "bg-red-300 hover:bg-red-500 text-white font-bold rounded"
};

    const ButtonSize = {
    sm: "py-2 px-4 text-xs",
    lg: "py-3 px-6 text-lg"
};

  // This can be improved. I’m keeping it simple here by joining two strings.
    const classNames = (ButtonType[type] || ButtonType.basic) + " " + (ButtonSize[size] || ButtonSize.sm);

    return (
    <button className={classNames}>
        {children}
    </button>
    )
}
