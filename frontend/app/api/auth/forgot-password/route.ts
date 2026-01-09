// import { NextResponse } from "next/server";
// import { connectDB } from "@/lib/db";
// import User from "@/models/User";
// import crypto from "crypto";

// export async function POST(req: Request) {
//   try {
//     const { email } = await req.json();

//     if (!email) {
//       return NextResponse.json(
//         { message: "Email is required" },
//         { status: 400 }
//       );
//     }

//     await connectDB();

//     const user = await User.findOne({ email });

//     if (!user) {
//       // Security: don't reveal user existence
//       return NextResponse.json({
//         message: "If account exists, reset link sent",
//       });
//     }

//     const token = crypto.randomBytes(32).toString("hex");
//     const hashedToken = crypto
//       .createHash("sha256")
//       .update(token)
//       .digest("hex");

//     user.resetPasswordToken = hashedToken;
//     user.resetPasswordExpiry = new Date(Date.now() + 15 * 60 * 1000);
//     await user.save();

//     console.log(
//       `RESET LINK: ${process.env.NEXTAUTH_URL}/reset-password?token=${token}`
//     );

//     return NextResponse.json({
//       message: "Password reset link sent",
//     });
//   } catch {
//     return NextResponse.json(
//       { message: "Something went wrong" },
//       { status: 500 }
//     );
//   }
// }


import { NextResponse } from "next/server";
import { connectDB } from "@/lib/db";
import User from "@/models/User";
import crypto from "crypto";
import { sendPasswordResetEmail } from "@/lib/email";

export async function POST(req: Request) {
  try {
    const { email } = await req.json();

    if (!email) {
      return NextResponse.json(
        { message: "Email is required" },
        { status: 400 }
      );
    }

    await connectDB();

    const user = await User.findOne({ email });

    if (!user) {
      // Security: don't reveal user existence
      return NextResponse.json({
        message: "If account exists, reset link sent",
      });
    }

    const token = crypto.randomBytes(32).toString("hex");
    const hashedToken = crypto
      .createHash("sha256")
      .update(token)
      .digest("hex");

    user.resetPasswordToken = hashedToken;
    user.resetPasswordExpiry = new Date(Date.now() + 15 * 60 * 1000);
    await user.save();

    // Send password reset email
    const emailResult = await sendPasswordResetEmail(user.email, token);
    if (!emailResult.success) {
      console.error("Failed to send password reset email:", emailResult.error);
      return NextResponse.json(
        { message: "Failed to send reset email" },
        { status: 500 }
      );
    }

    return NextResponse.json({
      message: "Password reset link sent to your email",
    });
  } catch {
    return NextResponse.json(
      { message: "Something went wrong" },
      { status: 500 }
    );
  }
}