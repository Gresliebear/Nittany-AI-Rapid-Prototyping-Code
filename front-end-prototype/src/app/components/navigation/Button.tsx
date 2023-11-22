import  {useRouter} from "next/navigation";

const Button = () => {
    const router = useRouter()
    
    const handleButtonClick = () => {
      router.push("/sign-in");
    };

    return (
      <button 
      onClick={handleButtonClick}
      className="h-12 rounded-lg bg-white font-bold px-5">
        Sign In
    </button>
    );
  };
  export default Button;