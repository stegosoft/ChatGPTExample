namespace ShapeAreaCalculator
{
    public interface IShape
    {
        double CalculateArea();
    }

    public class Rectangle : IShape
    {
        public double Width { get; set; }
        public double Height { get; set; }

        public Rectangle(double width, double height)
        {
            Width = width;
            Height = height;
        }

        /*        
            Calculate the area of a given rectangle.
            
            Parameters:
                None
            
            Returns:
                float: The area of the rectangle.
        */
        public double CalculateArea()
        {
            return Width * Height;
        }
    }

    public class Circle : IShape
    {
        public double Radius { get; set; }

        public Circle(double radius)
        {
            Radius = radius;
        }

        /*        
            Calculates the area of a circle.
            
            Parameters:
                None
            
            Returns:
                double: The area of the circle.
        */
        public double CalculateArea()
        {
            return Math.PI * Math.Pow(Radius, 2);
        }
    }

    public class Triangle : IShape
    {
        public double Base { get; set; }
        public double Height { get; set; }

        public Triangle(double baseLength, double height)
        {
            Base = baseLength;
            Height = height;
        }

        /*        
            Calculate the area of a triangle given the base and height.
            
            Parameters:
                Base (double): The base of the triangle.
                Height (double): The height of the triangle.
                
            Returns:
                double: The area of the triangle.
        */
        public double CalculateArea()
        {
            return 0.5 * Base * Height;
        }
    }

}
